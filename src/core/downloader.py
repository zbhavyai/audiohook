import os
import re
from pathlib import Path

import yt_dlp

from src.config import get_logger
from src.core.metadata import set_metadata
from src.utils.csv_handler import read_csv

logger = get_logger(__name__)


def download_audio(
    yt_link: str, start_time: str, end_time: str, file_name: str, output_directory: str | Path
) -> tuple[bool, str | None]:
    """
    Downloads audio from a YouTube link and saves it as an audio file in the specified output directory.
    Args:
        yt_link (str): The URL of the YouTube video to download.
        file_name (str): The desired name for the downloaded audio file (without extension).
        output_directory (str | Path): The directory where the downloaded audio file will be saved.
    Returns:
        Tuple[bool, str | None]: A tuple containing:
            - bool: True if the download was successful, False otherwise.
            - str | None: The path to the downloaded audio file, or None if download failed.
    """
    logger.debug(f'downloading: "{yt_link}" into "{output_directory}"')

    out_dir = Path(output_directory)
    if not out_dir.exists():
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f'created directory: "{output_directory}"')
        except OSError as e:
            logger.error(f'error creating directory "{output_directory}": {e}')
            return (False, None)

    final_filename = None

    def progress_hook(d: dict) -> None:
        if d["status"] == "finished":
            logger.debug(f'finished downloading "{os.path.basename(d["filename"])}"')

    def postprocessor_hook(d: dict) -> None:
        nonlocal final_filename
        if d["status"] == "finished" and d["postprocessor"] == "MoveFiles":
            final_filename = d["info_dict"]["filepath"]
            logger.debug(f'finished processing "{os.path.basename(final_filename)}"')

    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{output_directory}/{file_name}.%(ext)s",
        "progress_hooks": [progress_hook],
        "postprocessor_hooks": [postprocessor_hook],
        "quiet": True,
        "noprogress": True,
    }

    # ffmpeg makes downloading too slow, don't use it
    # trim_opts = []
    # if start_time and start_time != "00:00:00":
    #     trim_opts += ["-ss", start_time]
    # if end_time and end_time != "00:00:00":
    #     trim_opts += ["-to", end_time]

    # if trim_opts:
    #     ydl_opts["external_downloader"] = "ffmpeg"
    #     ydl_opts["external_downloader_args"] = {"default": trim_opts}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_link])

            if final_filename:
                just_filename = os.path.basename(final_filename)
                logger.info(f'downloaded "{yt_link}" as "{just_filename}"')

        if final_filename and os.path.exists(final_filename):
            return (True, final_filename)
        return (False, None)

    except yt_dlp.DownloadError as e:
        logger.error(f'download error for "{file_name}": {e}')
        return (False, None)

    except Exception as e:
        logger.error(f"an error occurred: {e}")
        return (False, None)


def download_audio_from_csv(file_path: str, output_directory: str | Path) -> None:
    """
    Downloads audio files from YouTube links specified in a CSV file.
    Args:
        file_path (str): The path to the CSV file containing YouTube links.
        output_directory (str | Path): The directory where the downloaded audio files will be saved.
    Returns:
        None
    """
    logger.debug(f'downloading audio from "{file_path}" into "{output_directory}"')

    headers, data = read_csv(file_path)

    def get_video_id(url: str) -> str | None:
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    for row in data:
        ytLink = row.get("ytLink")
        if not ytLink:
            continue
        title = row.get("title")
        video_id = get_video_id(ytLink)
        start_time = row.get("start_time", "")
        end_time = row.get("end_time", "")
        (status, file) = download_audio(ytLink, start_time, end_time, f"{title} - {video_id}", output_directory)

        if status and file is not None:
            set_metadata(
                file,
                row["title"],
                row["artist"],
                row["album"],
                row["composer"],
                row["year"],
                row["genre"],
                row["ytLink"],
            )
