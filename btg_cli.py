import argparse
import os
import logging
from common import download_audio, pitch_shift, separate_stems, create_beat_track, create_backing_track, add_start_beat_to_audio


def main():
    parser = argparse.ArgumentParser(description="Backing Track Generator CLI: Download/process audio, separate stems, create beat/backing tracks.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--youtube-url", help="URL of the YouTube video to download audio from.")
    group.add_argument("--file-name", help="Path to a local audio file to process.")
    parser.add_argument("--output", default="output", help="Output folder for the processed files.")
    parser.add_argument("--shift", type=int, default=0, help="Number of semitones to shift the audio.")
    parser.add_argument("--model", default="htdemucs_ft", help="Demucs model to use for stem separation.")
    parser.add_argument("--exclude", help="Stem to exclude when creating the backing track (e.g., 'vocals').")
    parser.add_argument("--include-beat", action="store_true", help="Include the beat track in the backing track generation.")
    parser.add_argument("--add-start-beat", action="store_true", help="Add a starting metronome beat to the mixed track.")
    parser.add_argument("--start-beat-clicks", type=int, default=4, help="Number of clicks for the starting beat (default: 4).")
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading if the audio file already exists.")

    args = parser.parse_args()

    # Validate mutually exclusive input
    if args.youtube_url and args.file_name:
        raise ValueError("You must provide only one of --youtube-url or --file-name, not both.")

    # Step 1: Get audio file (download or local)
    if args.youtube_url:
        audio_file, working_folder = download_audio(args.youtube_url, args.output)
    else:
        audio_file = args.file_name
        working_folder = args.output

    # Step 2: Pitch shift if required
    if args.shift != 0:
        audio_file = pitch_shift(audio_file, args.shift, working_folder)

    # Step 3: Separate stems using Demucs
    stems_folder = separate_stems(audio_file, args.model, working_folder)

    # Step 4: Create beat track
    beat_track_file = create_beat_track(audio_file, working_folder)

    # Step 5: Create backing tracks (with and without beat if requested)
    backing_track_file = None
    backing_track_with_beat = None
    if args.exclude:
        logging.info(f"Generating track excluding [{args.exclude}] (without beat track)...")
        backing_track_file = create_backing_track(stems_folder, args.exclude, working_folder, include_beat=False)
        if args.include_beat:
            logging.info(f"Generating track excluding [{args.exclude}] (with beat track)...")
            backing_track_with_beat = create_backing_track(stems_folder, args.exclude, working_folder, include_beat=True, beat_file=beat_track_file)

    # Step 6: Add start beat to the mixed tracks and beat track if requested
    if args.add_start_beat:
        # Add to beat track itself
        if beat_track_file:
            beat_track_with_start = beat_track_file.replace('.mp3', '_with_start_beat.mp3')
            add_start_beat_to_audio(beat_track_file, beat_track_with_start, num_beats=args.start_beat_clicks)
            logging.info(f"Beat track with start beat created: {beat_track_with_start}")
        # Add to backing track without beat
        if backing_track_file:
            output_with_start_beat = backing_track_file.replace('.mp3', '_with_start_beat.mp3')
            add_start_beat_to_audio(backing_track_file, output_with_start_beat, num_beats=args.start_beat_clicks)
            logging.info(f"Backing track (no beat) with start beat created: {output_with_start_beat}")
        # Add to backing track with beat
        if backing_track_with_beat:
            output_with_start_beat_beat = backing_track_with_beat.replace('.mp3', '_with_start_beat.mp3')
            add_start_beat_to_audio(backing_track_with_beat, output_with_start_beat_beat, num_beats=args.start_beat_clicks)
            logging.info(f"Backing track (with beat) with start beat created: {output_with_start_beat_beat}")

    logging.info("Finished processing audio!")

if __name__ == "__main__":
    main()
