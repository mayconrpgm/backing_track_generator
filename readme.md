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

### Download and Process YouTube Audio
To download a YouTube video, apply pitch shifting, separate stems, create a beat track, and optionally generate a backing track:

```
python download_and_process.py <YouTube_URL> --output <output_folder> --shift <semitones> --model <demucs_model> --exclude <stem_to_exclude> --include-beat`
```

- `YouTube_URL`: The URL of the YouTube video.
- `output_folder`: Where to save processed files.
- `shift`: Number of semitones to shift up or down.
- `model`: Demucs model for separation.
- `exclude`: Stem to exclude when creating the backing track (e.g., `vocals`).
- `include-beat`: Flag to add the beat track to the backing track.

### Process Local Audio File
To process a local audio file with the same options:

```
python process_local_file.py <audio_file_path> --output <output_folder> --shift <semitones> --model <demucs_model> --exclude <stem_to_exclude> --include-beat
```


## Example Workflows

### 1. Download a YouTube Song and Create a Voice Backing Track

```
python download_and_process.py "https://www.youtube.com/watch?v=example" --output music_output --shift -2 --model htdemucs --exclude vocals --include-beat
```


### 2. Process a Local File and Create a Drumless Backing Track

```
python process_local_file.py "my_song.mp3" --output music_output --shift 3 --model htdemucs --exclude drums
```

## Additional Information
For more details on how to configure `demucs`, check the [Demucs GitHub repository](https://github.com/adefossez/demucs).
