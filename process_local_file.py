# process_local_file.py
import argparse
import os
from common import pitch_shift, separate_stems, create_beat_track

def main():
    parser = argparse.ArgumentParser(description="Process a local audio file: pitch shift, create beat track, and separate stems.")
    parser.add_argument('audio_file', help="Path to the local audio file")
    parser.add_argument('--output', default='processed/', help="Output directory for processing")
    parser.add_argument('--shift', type=int, default=0, help="Pitch shift in semitones")
    parser.add_argument('--model', default='mdx_extra', help="Demucs model to use for stem separation")

    args = parser.parse_args()

    try:
        output_folder = os.path.join(args.output, os.path.splitext(os.path.basename(args.audio_file))[0])
        os.makedirs(output_folder, exist_ok=True)

        if args.shift != 0:
            print(f"Pitch shifting by {args.shift} semitones...")
            shifted_file = pitch_shift(args.audio_file, args.shift, output_folder)
            print(f"Pitch-shifted file: {shifted_file}")
        else:
            shifted_file = args.audio_file

        print("Creating beat track...")
        beat_track_file = create_beat_track(shifted_file, output_folder)
        print(f"Beat track created: {beat_track_file}")

        print("Separating stems...")
        stems_output = separate_stems(shifted_file, args.model, output_folder)
        print(f"Stems saved to: {stems_output}")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
