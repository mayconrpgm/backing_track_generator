import argparse
import os
import subprocess
import librosa
import soundfile as sf

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
    parser = argparse.ArgumentParser(description="Process a local audio file: pitch shift and separate stems.")
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

        print("Separating stems...")
        stems_output = separate_stems(shifted_file, args.model, output_folder)
        print(f"Stems saved to: {stems_output}")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
