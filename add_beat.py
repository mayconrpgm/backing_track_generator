import librosa
import os
import numpy as np
import soundfile as sf

def generate_click_sound(duration, sr):
    """Generate a short click sound."""
    # Generate a sine wave as the click sound
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    click = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    return click

def add_start_beat_to_audio(input_file, output_file, num_beats=4):
    """Add a specified number of metronome beats to the start of an audio file."""
    # Load the original audio
    audio, sr = librosa.load(input_file, sr=None)

    # Remove leading and trailing silence
    audio, _ = librosa.effects.trim(audio, top_db=20)

    # Automatically detect the tempo of the audio
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
    print(f"Detected tempo: {tempo} BPM")

    # Calculate the duration of each beat in seconds
    beat_duration = 60.0 / tempo

    # Generate the click sound for one beat
    click_sound = generate_click_sound(duration=0.1, sr=sr)  # 100 ms click

    # Create a silent segment to separate clicks (duration of beat minus click duration)
    silence_duration = max(0, beat_duration - 0.1)
    silence_length = int(float(sr * silence_duration))  # Ensure it's a scalar integer
    silence = np.zeros(silence_length, dtype=np.float32)

    # Create the full metronome beat pattern (alternating click + silence)
    metronome = np.concatenate([np.concatenate([click_sound, silence]) for _ in range(num_beats)])

    # Concatenate the metronome with the original audio
    output_audio = np.concatenate([metronome, audio])

    # Save the output audio to a file
    sf.write(output_file, output_audio, sr)

    print(f"Audio saved to {output_file} with {num_beats} beats added at the detected tempo of {tempo} BPM.")

def add_beats_to_audio_v2(input_file, output_file, num_beats=4):
    """Add a specified number of metronome beats to the start of an audio file."""
    # Load the original audio
    audio, sr = librosa.load(input_file, sr=None)

    # Remove leading and trailing silence
    audio, _ = librosa.effects.trim(audio, top_db=20)

    # Automatically detect the tempo and beat positions of the audio
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
    print(f"Detected tempo: {tempo} BPM")

    # Convert the beat frames to time (in seconds)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Generate the click track for the initial beats
    initial_beats = np.linspace(0, (num_beats - 1) * (60.0 / tempo), num=num_beats)
    click_track_start = librosa.clicks(times=initial_beats, sr=sr, length=len(audio) + int(sr * initial_beats[-1]))

    # Add the initial click track to the start of the audio
    output_audio = click_track_start + np.pad(audio, (len(click_track_start) - len(audio), 0), mode='constant')

    # Save the output audio to a file
    sf.write(output_file, output_audio, sr)

    print(f"Audio saved to {output_file} with {num_beats} beats added at the detected tempo of {tempo} BPM.")

# Example usage
input_audio_folder = 'input_path'
input_file_name = 'input_file'
input_audio_path = os.path.join(input_audio_folder, input_file_name)
output_audio_path = os.path.join(input_audio_folder, input_file_name.replace('.mp3', '_with_start_beat.mp3'))
output_audio_path_v2 = os.path.join(input_audio_folder, input_file_name.replace('.mp3', '_with_start_beat_v2.mp3'))

#add_start_beat_to_audio(input_audio_path, output_audio_path)
add_beats_to_audio_v2(input_audio_path, output_audio_path_v2, num_beats=8)

