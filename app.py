import argparse
import os
import subprocess
from pytubefix import YouTube
import librosa
import soundfile as sf

def download_audio(youtube_url, output_path='downloads/', skip_download=False):
    try:
        yt = YouTube(youtube_url)
        video_title = yt.title
        mp3_file = os.path.join(output_path, f"{video_title}.mp3")

        # Check if the file already exists
        if os.path.exists(mp3_file):
            if skip_download:
                print(f"Audio file '{mp3_file}' already exists. Skipping download.")
                return mp3_file

            # Ask the user if they want to re-download the file
            response = input(f"Audio file '{mp3_file}' already exists. Do you want to re-download it? (y/n): ").strip().lower()
            if response != 'y':
                print("Using the existing audio file.")
                return mp3_file

        # Download the audio
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path=output_path)
        base, ext = os.path.splitext(audio_file)
        os.rename(audio_file, mp3_file)
        return mp3_file
    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {str(e)}")

def separate_stems(audio_file, output_path='stems/'):
    try:
        subprocess.run(['demucs', '-o', output_path, audio_file], check=True)
        return os.path.join(output_path, os.path.basename(audio_file).replace('.mp3', ''))
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Stem separation failed: {str(e)}")

def pitch_shift(audio_file, semitones, output_file='shifted_output.wav'):
    try:
        y, sr = librosa.load(audio_file, sr=None)
        y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=semitones)
        sf.write(output_file, y_shifted, sr)
        return output_file
    except Exception as e:
        raise RuntimeError(f"Pitch shifting failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="CLI tool for music stem separation and pitch shifting.")
    parser.add_argument('url', help="YouTube URL of the video to download")
    parser.add_argument('--output', help="Output directory for downloads and processing", default='downloads/')
    parser.add_argument('--shift', type=int, help="Pitch shift in semitones", default=0)
    parser.add_argument('--skip-download', action='store_true', help="Automatically skip downloading if the audio file already exists")

    args = parser.parse_args()

    try:
        print("Downloading audio...")
        audio_file = download_audio(args.url, args.output, args.skip_download)
        print(f"Audio downloaded: {audio_file}")

        print("Separating stems...")
        stems_dir = separate_stems(audio_file, args.output)
        print(f"Stems saved to: {stems_dir}")

        if args.shift != 0:
            print(f"Pitch shifting by {args.shift} semitones...")
            shifted_file = pitch_shift(audio_file, args.shift, os.path.join(args.output, 'shifted_output.wav'))
            print(f"Pitch-shifted file saved to: {shifted_file}")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
