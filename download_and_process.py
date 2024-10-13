import argparse
import os
import subprocess
from pytubefix import YouTube
import librosa
import soundfile as sf

def download_audio(youtube_url, output_path):
    try:
        yt = YouTube(youtube_url)
        video_title = yt.title
        download_folder = os.path.join(output_path, video_title)
        os.makedirs(download_folder, exist_ok=True)

        mp3_file = os.path.join(download_folder, f"{video_title}.mp3")
        if os.path.exists(mp3_file):
            print(f"Audio file '{mp3_file}' already exists. Skipping download.")
            return mp3_file, download_folder

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path=download_folder)
        base, ext = os.path.splitext(audio_file)
        os.rename(audio_file, mp3_file)
        return mp3_file, download_folder
    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {str(e)}")

def pitch_shift(audio_file, semitones, output_folder):
    try:
        shifted_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(audio_file))[0]}_{semitones:+}st.mp3")
        if os.path.exists(shifted_file):
            print(f"Pitch-shifted file '{shifted_file}' already exists. Skipping.")
            return shifted_file

        y, sr = librosa.load(audio_file, sr=None)
        y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=semitones)
        sf.write(shifted_file, y_shifted, sr)
        return shifted_file
    except Exception as e:
        raise RuntimeError(f"Pitch shifting failed: {str(e)}")

def separate_stems(audio_file, model, output_folder):
    try:
        stems_output = os.path.join(output_folder, 'stems')
        if not os.path.exists(stems_output):
            os.makedirs(stems_output)

        subprocess.run(['demucs', '-n', model, '--mp3', '-o', stems_output, audio_file], check=True)
        return stems_output
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Stem separation failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Download audio, pitch shift, and separate stems.")
    parser.add_argument('url', help="YouTube URL of the video to download")
    parser.add_argument('--output', default='downloads/', help="Output directory for downloads and processing")
    parser.add_argument('--shift', type=int, default=0, help="Pitch shift in semitones")
    parser.add_argument('--model', default='mdx_extra', help="Demucs model to use for stem separation")

    args = parser.parse_args()

    try:
        print("Downloading audio...")
        audio_file, download_folder = download_audio(args.url, args.output)
        print(f"Audio downloaded: {audio_file}")

        if args.shift != 0:
            print(f"Pitch shifting by {args.shift} semitones...")
            audio_file = pitch_shift(audio_file, args.shift, download_folder)
            print(f"Pitch-shifted file: {audio_file}")

        print("Separating stems...")
        stems_output = separate_stems(audio_file, args.model, download_folder)
        print(f"Stems saved to: {stems_output}")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
