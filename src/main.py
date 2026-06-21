import click

from src.config import OUTPUT_DIR, VERSION, get_logger
from src.core.downloader import download_audio, download_audio_from_csv
from src.core.metadata import clean_metadata, print_metadata, set_metadata
from src.utils.csv_handler import read_csv
from src.utils.table import display_data

logger = get_logger(__name__)


@click.group(help="A script to download audio from YouTube links.")
@click.version_option(version=VERSION, message="version: %(version)s")
def main() -> None:
    """A script to download audio from YouTube links."""
    pass


@main.group(help="Manipulate metadata of audio files")
def metadata() -> None:
    pass


@metadata.command(name="print", help="Print metadata of a file or directory")
@click.option("--file", required=True, help="File or directory path")
def metadata_print(file: str) -> None:
    print_metadata(file)


@metadata.command(name="clean", help="Clean metadata from a file or directory")
@click.option("--file", required=True, help="File or directory path")
def metadata_clean(file: str) -> None:
    clean_metadata(file)


@metadata.command(name="set", help="Set metadata for a file or directory")
@click.option("--file", required=True, help="File or directory path")
@click.option("--title", default="", help="Title of the audio")
@click.option("--album", default="", help="Album name")
@click.option("--artist", default="", help="Artist name")
@click.option("--composer", default="", help="Composer name")
@click.option("--year", default="", help="Year of release")
@click.option("--comment", default="", help="Comment")
@click.option("--genre", default="", help="Genre")
def metadata_set(
    file: str,
    title: str,
    album: str,
    artist: str,
    composer: str,
    year: str,
    comment: str,
    genre: str,
) -> None:
    set_metadata(
        file_path=file,
        title=title,
        artist=artist,
        album=album,
        composer=composer,
        year=year,
        genre=genre,
        comments=comment,
    )


@main.command(help="Download audio from YouTube URL")
@click.option("--url", required=True, help="YouTube video URL")
@click.option("--output", required=True, help="Output file path")
def download(url: str, output: str) -> None:
    download_audio(url, "00:00:00", "00:00:00", output, OUTPUT_DIR)


@main.command(help="Trim an audio file")
@click.option("--file", required=True, help="Input file path")
@click.option("--start", required=True, help="Start time (in seconds)")
@click.option("--end", required=True, help="End time (in seconds)")
@click.option("--output", required=True, help="Output file path")
def trim(file: str, start: str, end: str, output: str) -> None:
    logger.error("Trimming is not implemented yet.")


@main.command(help="Process CSV file")
@click.option("--file", required=True, help="CSV file path")
@click.option("--print", "print_data_flag", is_flag=True, help="Print CSV data")
@click.option("--download", "download_flag", is_flag=True, help="Download from CSV file")
def csv(file: str, print_data_flag: bool, download_flag: bool) -> None:
    if print_data_flag:
        headers, data = read_csv(file)
        display_data(headers, data)
    elif download_flag:
        download_audio_from_csv(file, OUTPUT_DIR)


@main.command(help="Print version")
def version() -> None:
    logger.info("Version: %s", VERSION)
    click.echo(VERSION)


if __name__ == "__main__":
    main()
