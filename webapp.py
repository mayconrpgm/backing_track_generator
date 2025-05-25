import os
import shutil
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from common import download_audio, pitch_shift, separate_stems, create_beat_track, create_backing_track, add_start_beat_to_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Steps for progress tracking
PROCESS_STEPS = [
    'Download Audio',
    'Pitch Shift',
    'Separate Stems',
    'Create Beat Track',
    'Create Backing Tracks',
    'Add Start Beat',
    'Packaging Results'
]

progress = { 'step': 0, 'message': 'Waiting for input...' }

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', steps=PROCESS_STEPS)

@app.route('/process', methods=['POST'])
def process():
    global progress
    progress = { 'step': 0, 'message': 'Starting...' }
    form = request.form
    files = request.files
    output_dir = tempfile.mkdtemp()
    artifacts = []
    try:
        # Step 1: Download or upload audio
        progress = { 'step': 1, 'message': 'Getting audio file...' }
        youtube_url = form.get('youtube_url')
        file = files.get('audio_file')
        if youtube_url:
            audio_file, working_folder = download_audio(youtube_url, output_dir)
        elif file:
            filename = secure_filename(file.filename)
            audio_file = os.path.join(output_dir, filename)
            file.save(audio_file)
            working_folder = output_dir
        else:
            return jsonify({'error': 'No audio source provided.'}), 400
        artifacts.append(audio_file)

        # Step 2: Pitch shift
        shift = int(form.get('shift', 0))
        progress = { 'step': 2, 'message': 'Pitch shifting...' }
        if shift != 0:
            audio_file = pitch_shift(audio_file, shift, working_folder)
            artifacts.append(audio_file)

        # Step 3: Separate stems
        model = form.get('model', 'htdemucs_ft')
        progress = { 'step': 3, 'message': 'Separating stems...' }
        stems_folder = separate_stems(audio_file, model, working_folder)
        artifacts.append(stems_folder)

        # Step 4: Create beat track
        progress = { 'step': 4, 'message': 'Creating beat track...' }
        beat_track_file = create_beat_track(audio_file, working_folder)
        artifacts.append(beat_track_file)

        # Step 5: Create backing tracks
        exclude = form.get('exclude')
        include_beat = form.get('include_beat') == 'on'
        backing_track_file = None
        backing_track_with_beat = None
        if exclude:
            progress = { 'step': 5, 'message': 'Creating backing tracks...' }
            backing_track_file = create_backing_track(stems_folder, exclude, working_folder, include_beat=False)
            artifacts.append(backing_track_file)
            if include_beat:
                backing_track_with_beat = create_backing_track(stems_folder, exclude, working_folder, include_beat=True, beat_file=beat_track_file)
                artifacts.append(backing_track_with_beat)

        # Step 6: Add start beat
        add_start_beat = form.get('add_start_beat') == 'on'
        start_beat_clicks = int(form.get('start_beat_clicks', 4))
        if add_start_beat:
            progress = { 'step': 6, 'message': 'Adding start beat...' }
            if beat_track_file:
                beat_track_with_start = beat_track_file.replace('.mp3', '_with_start_beat.mp3')
                add_start_beat_to_audio(beat_track_file, beat_track_with_start, num_beats=start_beat_clicks)
                artifacts.append(beat_track_with_start)
            if backing_track_file:
                output_with_start_beat = backing_track_file.replace('.mp3', '_with_start_beat.mp3')
                add_start_beat_to_audio(backing_track_file, output_with_start_beat, num_beats=start_beat_clicks)
                artifacts.append(output_with_start_beat)
            if backing_track_with_beat:
                output_with_start_beat_beat = backing_track_with_beat.replace('.mp3', '_with_start_beat.mp3')
                add_start_beat_to_audio(backing_track_with_beat, output_with_start_beat_beat, num_beats=start_beat_clicks)
                artifacts.append(output_with_start_beat_beat)

        # Step 7: Package results
        progress = { 'step': 7, 'message': 'Packaging results...' }
        zip_path = os.path.join(working_folder, 'results.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for artifact in artifacts:
                if os.path.isdir(artifact):
                    for root, _, files in os.walk(artifact):
                        for f in files:
                            zipf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), working_folder))
                else:
                    zipf.write(artifact, os.path.relpath(artifact, working_folder))
        progress = { 'step': 7, 'message': 'Done!' }
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        progress = { 'step': 7, 'message': f'Error: {str(e)}' }
        return jsonify({'error': str(e)}), 500
    finally:
        # Optionally clean up temp files after download
        pass

@app.route('/progress')
def get_progress():
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True)
