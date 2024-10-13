# download_and_process.py
import argparse
import os
from common import download_audio, pitch_shift, separate_stems, create_beat_track

def main():
    parser = argparse.ArgumentParser(description="Download audio, pitch shift, create beat track, and separate stems.")
    parser.add_argument('url', help="YouTube URL of the video to download")
    parser.add_argument('--output', default='downloads/', help="Output directory for downloads and processing")
    parser.add_argument('--shift', type=int, default=0, help="Pitch shift in semitones")
    parser.add_argument('--model', default='hdemucs_mmi', help="Demucs model to use for stem separation")

    args = parser.parse_args()

    try:
        print("Downloading audio...")
        audio_file, download_folder = download_audio(args.url, args.output)
        print(f"Audio downloaded: {audio_file}")

        if args.shift != 0:
            print(f"Pitch shifting by {args.shift} semitones...")
            audio_file = pitch_shift(audio_file, args.shift, download_folder)
            print(f"Pitch-shifted file: {audio_file}")

        print("Creating beat track...")
        beat_track_file = create_beat_track(audio_file, download_folder)
        print(f"Beat track created: {beat_track_file}")

        print("Separating stems...")
        stems_output = separate_stems(audio_file, args.model, download_folder)
        print(f"Stems saved to: {stems_output}")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
