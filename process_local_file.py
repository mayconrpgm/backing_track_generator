import argparse
import os
from common import pitch_shift, separate_stems, create_beat_track, create_backing_track

def main():
    parser = argparse.ArgumentParser(description="Process local audio file: pitch shifting, stem separation, and create a backing track.")
    parser.add_argument("audio_file", help="Path to the local audio file to process.")
    parser.add_argument("--output", default="output", help="Output folder for the processed files.")
    parser.add_argument("--shift", type=int, default=0, help="Number of semitones to shift the audio.")
    parser.add_argument("--model", default="htdemucs_ft", help="Demucs model to use for stem separation.")
    parser.add_argument("--exclude", help="Stem to exclude when creating the backing track (e.g., 'vocals').")
    parser.add_argument("--include-beat", action="store_true", help="Include the beat track in the backing track generation.")
    
    args = parser.parse_args()

    # Step 1: Pitch shift if required
    audio_file = args.audio_file
    if args.shift != 0:
        audio_file = pitch_shift(audio_file, args.shift, args.output)

    # Step 2: Separate stems using Demucs
    stems_folder = separate_stems(audio_file, args.model, args.output)

    # Step 3: Create beat track
    beat_track_file = create_beat_track(audio_file, args.output)

    # Step 4: Create backing track if specified
    if args.exclude:
        backing_track_with_beat = None
        backing_track_without_beat = create_backing_track(stems_folder, args.exclude, args.output, include_beat_track=False)
        if args.include_beat:
            backing_track_with_beat = create_backing_track(stems_folder, args.exclude, args.output, include_beat_track=True)

        print(f"Backing track excluding '{args.exclude}' created: {backing_track_without_beat}")
        if backing_track_with_beat:
            print(f"Backing track with beat excluding '{args.exclude}' created: {backing_track_with_beat}")

if __name__ == "__main__":
    main()
