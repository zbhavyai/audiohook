# AudioHook

Download YouTube audio, curate metadata tags, and batch-process tracks.

## Features

- **Metadata Management**: Print, clean, and set ID3 tags.
- **YouTube Audio Download**: Download audio from a YouTube URL.
- **CSV Processing**: Perform bulk operations based on a CSV file.

## Installation

1. Install dependencies

   ```shell
   make init
   ```

2. Print the version to verify installation:

   ```shell
   make print-version
   ```

## Usage

Run the command using

```shell
uv run audiohook <group> <action> [options]
```

> [!NOTE]
> Alternatively, you can run the package module directly using `uv run python -m src.audiohook <group> <action> [options]`, or activate the virtual environment (`source .venv/bin/activate`) and run `audiohook <group> <action> [options]`.

### Command Groups & Actions

#### 1. Metadata Operations

```shell
uv run audiohook metadata print --file <FILE_OR_DIRECTORY>

uv run audiohook metadata clean --file <FILE_OR_DIRECTORY>

uv run audiohook metadata set --file <FILE_OR_DIRECTORY> \
    --title <TITLE> \
    --artist <ARTIST> \
    --year <YEAR> \
    --composer <COMPOSER> \
    --comment <COMMENT> \
    --genre <GENRE> \
    --album <ALBUM>
```

#### 2. Download Audio from YouTube

```shell
uv run audiohook download --url <YOUTUBE_URL> --output <OUTPUT_FILE>
```

#### 3. CSV Processing

```shell
uv run audiohook csv --file <CSV_FILE> --print
uv run audiohook csv --file <CSV_FILE> --download
```
