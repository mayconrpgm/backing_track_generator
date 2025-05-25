# Music Processing CLI Tool

This tool allows you to download audio from YouTube, apply pitch shifting, separate tracks into individual stems (such as vocals, bass, etc.), create a beat track, and generate backing tracks for practice sessions.

## Features
- **Download audio from YouTube**: Supports downloading audio directly from a given YouTube URL.
- **Pitch shifting**: Change the pitch of the audio by a specified number of semitones.
- **Stem separation**: Use `demucs` to split the audio into individual instrument tracks.
- **Create beat track**: Generate a click track aligned with the beats of the song, with an additional four initial beats for easier synchronization.
- **Generate backing tracks**: Mix all the stems together, optionally excluding one instrument (e.g., vocals) and including the beat track.

## Requirements
- Python 3.7 or later
- [ffmpeg](https://ffmpeg.org/)
- [pytubefix](https://pytubefix.readthedocs.io/en/latest/)
- [librosa](https://librosa.org/)
- [Demucs](https://github.com/adefossez/demucs)

### Installing Dependencies
1. Install Python and `ffmpeg`.
   - For `ffmpeg` installation:
     - **Windows**: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to your PATH.
     - **macOS**: Use Homebrew: `brew install ffmpeg`
     - **Linux**: Use your package manager, e.g., `sudo apt-get install ffmpeg`

2. Install Python libraries:

```
pip install -r requirements.txt
```

## Usage

### Download and Process YouTube Audio or Local File
To process audio (YouTube or local), apply pitch shifting, separate stems, create a beat track, and optionally generate a backing track:

```
python btg_cli.py --youtube-url <YouTube_URL> --output <output_folder> --shift <semitones> --model <demucs_model> --exclude <stem_to_exclude> --include-beat --add-start-beat --start-beat-clicks 4
```

or for a local file:

```
python btg_cli.py --file-name <audio_file_path> --output <output_folder> --shift <semitones> --model <demucs_model> --exclude <stem_to_exclude> --include-beat --add-start-beat --start-beat-clicks 4
```

- `--youtube-url`: The URL of the YouTube video.
- `--file-name`: Path to a local audio file.
- `--output`: Where to save processed files.
- `--shift`: Number of semitones to shift up or down.
- `--model`: Demucs model for separation.
- `--exclude`: Stem to exclude when creating the backing track (e.g., `vocals`).
- `--include-beat`: If set, generates both backing tracks with and without the beat track included.
- `--add-start-beat`: If set, adds a starting metronome beat to all output tracks (beat track, backing track with and without beat).
- `--start-beat-clicks`: Number of clicks for the starting beat (default: 4).

**Note:**
- When `--include-beat` is set, both versions of the backing track (with and without the beat track) are generated.
- When `--add-start-beat` is set, the start beat is added to the beat track, the backing track without beat, and the backing track with beat.

## Example Workflows

### 1. Download a YouTube Song and Create a Voice Backing Track with Start Beat

```
python btg_cli.py --youtube-url "https://www.youtube.com/watch?v=example" --output music_output --shift -2 --model htdemucs --exclude vocals --include-beat --add-start-beat --start-beat-clicks 4
```

### 2. Process a Local File and Create a Drumless Backing Track with Start Beat

```
python btg_cli.py --file-name "my_song.mp3" --output music_output --shift 3 --model htdemucs --exclude drums --include-beat --add-start-beat --start-beat-clicks 4
```

## Additional Information
For more details on how to configure `demucs`, check the [Demucs GitHub repository](https://github.com/adefossez/demucs).
