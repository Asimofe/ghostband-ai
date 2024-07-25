from flask import Flask, request, jsonify, send_file
import os
from spleeter.separator import Separator
import gc
import mido
from music21 import converter, instrument, stream
import subprocess


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
SHEET_FOLDER = "./sheet"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

GM_INSTRUMENTS = [
"Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano", "Electric Piano 1", "Electric Piano 2", "Harpsichord", "Clavinet", "Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer", "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accordion", "Harmonica", "Tango Accordion", "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar", "Guitar harmonics", "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass", "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2", "Violin", "Viola", "Cello", "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani", "String Ensemble 1", "String Ensemble 2", "SynthStrings 1", "SynthStrings 2", "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit", "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section", "SynthBrass 1", "SynthBrass 2", "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", "Bassoon", "Clarinet", "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina", "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)", "Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)", "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)", "Pad 5 (bowed)", "Pad 6 (metallic)", "Pad 7 (halo)", "Pad 8 (sweep)", "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)", "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)", "Sitar", "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle", "Shanai", "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal", "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter", "Applause", "Gunshot"
]

GM_INSTRUMENTS_CATEGORIZED = [
    ("Acoustic Grand Piano", "piano"),
    ("Bright Acoustic Piano", "piano"),
    ("Electric Grand Piano", "piano"),
    ("Honky-tonk Piano", "piano"),
    ("Electric Piano 1", "piano"),
    ("Electric Piano 2", "piano"),
    ("Harpsichord", "ETC"),
    ("Clavinet", "ETC"),
    ("Celesta", "keyboard"),
    ("Glockenspiel", "keyboard"),
    ("Music Box", "keyboard"),
    ("Vibraphone", "keyboard"),
    ("Marimba", "keyboard"),
    ("Xylophone", "keyboard"),
    ("Tubular Bells", "keyboard"),
    ("Dulcimer", "keyboard"),
    ("Drawbar Organ", "organ"),
    ("Percussive Organ", "organ"),
    ("Rock Organ", "organ"),
    ("Church Organ", "organ"),
    ("Reed Organ", "organ"),
    ("Accordion", "keyboard"),
    ("Harmonica", "keyboard"),
    ("Tango Accordion", "keyboard"),
    ("Acoustic Guitar (nylon)", "guitar"),
    ("Acoustic Guitar (steel)", "guitar"),
    ("Electric Guitar (jazz)", "guitar"),
    ("Electric Guitar (clean)", "guitar"),
    ("Electric Guitar (muted)", "guitar"),
    ("Overdriven Guitar", "guitar"),
    ("Distortion Guitar", "guitar"),
    ("Guitar harmonics", "guitar"),
    ("Acoustic Bass", "bass_guitar"),
    ("Electric Bass (finger)", "bass_guitar"),
    ("Electric Bass (pick)", "bass_guitar"),
    ("Fretless Bass", "bass_guitar"),
    ("Slap Bass 1", "bass_guitar"),
    ("Slap Bass 2", "bass_guitar"),
    ("Synth Bass 1", "bass_guitar"),
    ("Synth Bass 2", "bass_guitar"),
    ("Violin", "violin"),
    ("Viola", "ETC"),
    ("Cello", "cello"),
    ("Contrabass", "ETC"),
    ("Tremolo Strings", "ETC"),
    ("Pizzicato Strings", "ETC"),
    ("Orchestral Harp", "ETC"),
    ("Timpani", "ETC"),
    ("String Ensemble 1", "ETC"),
    ("String Ensemble 2", "ETC"),
    ("SynthStrings 1", "ETC"),
    ("SynthStrings 2", "ETC"),
    ("Choir Aahs", "ETC"),
    ("Voice Oohs", "ETC"),
    ("Synth Voice", "ETC"),
    ("Orchestra Hit", "ETC"),
    ("Trumpet", "trumpet"),
    ("Trombone", "ETC"),
    ("Tuba", "ETC"),
    ("Muted Trumpet", "trumpet"),
    ("French Horn", "ETC"),
    ("Brass Section", "ETC"),
    ("SynthBrass 1", "ETC"),
    ("SynthBrass 2", "ETC"),
    ("Soprano Sax", "sax"),
    ("Alto Sax", "sax"),
    ("Tenor Sax", "sax"),
    ("Baritone Sax", "sax"),
    ("Oboe", "ETC"),
    ("English Horn", "ETC"),
    ("Bassoon", "ETC"),
    ("Clarinet", "ETC"),
    ("Piccolo", "ETC"),
    ("Flute", "ETC"),
    ("Recorder", "ETC"),
    ("Pan Flute", "ETC"),
    ("Blown Bottle", "ETC"),
    ("Shakuhachi", "ETC"),
    ("Whistle", "ETC"),
    ("Ocarina", "ETC"),
    ("Lead 1 (square)", "synth"),
    ("Lead 2 (sawtooth)", "synth"),
    ("Lead 3 (calliope)", "synth"),
    ("Lead 4 (chiff)", "synth"),
    ("Lead 5 (charang)", "synth"),
    ("Lead 6 (voice)", "synth"),
    ("Lead 7 (fifths)", "synth"),
    ("Lead 8 (bass + lead)", "synth"),
    ("Pad 1 (new age)", "synth"),
    ("Pad 2 (warm)", "synth"),
    ("Pad 3 (polysynth)", "synth"),
    ("Pad 4 (choir)", "synth"),
    ("Pad 5 (bowed)", "synth"),
    ("Pad 6 (metallic)", "synth"),
    ("Pad 7 (halo)", "synth"),
    ("Pad 8 (sweep)", "synth"),
    ("FX 1 (비)", "synth"),
    ("FX 2 (soundtrack)", "synth"),
    ("FX 3 (crystal)", "synth"),
    ("FX 4 (atmosphere)", "synth"),
    ("FX 5 (brightness)", "synth"),
    ("FX 6 (goblins)", "synth"),
    ("FX 7 (echoes)", "synth"),
    ("FX 8 (sci-fi)", "synth"),
    ("Sitar", "ETC"),
    ("Banjo", "ETC"),
    ("Shamisen", "ETC"),
    ("Koto", "ETC"),
    ("Kalimba", "ETC"),
    ("Bag pipe", "ETC"),
    ("Fiddle", "ETC"),
    ("Shanai", "ETC"),
    ("Tinkle Bell", "ETC"),
    ("Agogo", "ETC"),
    ("Steel Drums", "ETC"),
    ("Woodblock", "ETC"),
    ("Taiko Drum", "drum"),
    ("Melodic Tom", "drum"),
    ("Synth Drum", "drum"),
    ("Reverse Cymbal", "drum"),
    ("Guitar Fret Noise", "ETC"),
    ("Breath Noise", "ETC"),
    ("Seashore", "ETC"),
    ("Bird Tweet", "ETC"),
    ("Telephone Ring", "ETC"),
    ("Helicopter", "ETC"),
    ("Applause", "ETC"),
    ("Gunshot", "ETC")
]

@app.route("/separator", methods=['POST'])
def separator_music():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    print(file.filename, flush=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    separator = Separator('spleeter:5stems')
    separator.separate_to_file(file_path, OUTPUT_FOLDER)
    output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0])
    
    file_names = [file for file in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, file))]
    
    file_urls = [ os.path.join(output_dir,file) for file in file_names]

    # files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    # file_urls = [url_for('download_file', filename=os.path.join(output_dir, f), _external=True) for f in files]

    del separator
    gc.collect()

    return jsonify({"file_urls": file_urls}), 200

@app.route("/download" , methods=["GET"])
def download_file():
    try:
        file_path = request.args.get('file_path')
        print(file_path, flush=True)

        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_path}"}), 404

        file_route = os.path.join("/home/jimmy/ghostBand/spleeter", file_path)
        print(file_route, flush=True)
        return send_file(file_route, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sheet", methods=["post"])
def midi2sheet():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    print(file.filename, flush=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    midi = mido.MidiFile(file_path)

    new_tracks = []
    instruments = set()
    instruments_cat = []

    for i, track in enumerate(midi.tracks):
        if any(msg.type != 'meta' for msg in track):
            new_tracks.append(track)
            for msg in track:
                if msg.type == 'program_change':
                    instruments.add(msg.program)
        else:
            print(f"Track {i} is empty and will be removed")

    new_midi = mido.MidiFile()
    new_midi.tracks.extend(new_tracks)

    output_midi_path = os.path.join(SHEET_FOLDER, "output.midi")

    new_midi.save(output_midi_path)
    print(f"New MIDI file saved as {output_midi_path}")

    base_filename = os.path.splitext(os.path.basename(file.filename))[0]
    output_pdf_filename = f"{base_filename}.pdf"

    output_pdf_path = os.path.join(SHEET_FOLDER, output_pdf_filename)
    print(output_pdf_path, flush=True)

    for i in instruments:
        instruments_cat.append(GM_INSTRUMENTS_CATEGORIZED[i][1])

    subprocess.run(["xvfb-run", "/usr/bin/musescore3", output_midi_path, "-o", output_pdf_path])

    return jsonify({"file_urls": output_pdf_path, "instruments": list(set(instruments_cat))}), 200
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')
