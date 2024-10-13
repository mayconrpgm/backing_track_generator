import argparse
import os
from common import download_audio, pitch_shift, separate_stems, create_beat_track, create_backing_track

def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio, process pitch shifting, stem separation, and create a backing track.")
    parser.add_argument("youtube_url", help="URL of the YouTube video to download audio from.")
    parser.add_argument("--output", default="output", help="Output folder for the processed files.")
    parser.add_argument("--shift", type=int, default=0, help="Number of semitones to shift the audio.")
    parser.add_argument("--model", default="htdemucs", help="Demucs model to use for stem separation.")
    parser.add_argument("--exclude", help="Stem to exclude when creating the backing track (e.g., 'vocals').")
    parser.add_argument("--include-beat", action="store_true", help="Include the beat track in the backing track generation.")
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading if the audio file already exists.")
    
    args = parser.parse_args()

    # Step 1: Download audio
    audio_file, download_folder = download_audio(args.youtube_url, args.output)

    # Step 2: Pitch shift if required
    if args.shift != 0:
        audio_file = pitch_shift(audio_file, args.shift, download_folder)

    # Step 3: Separate stems using Demucs
    stems_folder = separate_stems(audio_file, args.model, download_folder)

    # Step 4: Create beat track
    beat_track_file = create_beat_track(audio_file, download_folder)

    # Step 5: Create backing track if specified
    if args.exclude:
        backing_track_with_beat = None
        backing_track_without_beat = create_backing_track(stems_folder, args.exclude, download_folder, include_beat_track=False)
        if args.include_beat:
            backing_track_with_beat = create_backing_track(stems_folder, args.exclude, download_folder, include_beat_track=True)

        print(f"Backing track excluding '{args.exclude}' created: {backing_track_without_beat}")
        if backing_track_with_beat:
            print(f"Backing track with beat excluding '{args.exclude}' created: {backing_track_with_beat}")

if __name__ == "__main__":
    main()
