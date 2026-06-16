import numpy as np
import os

from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import load_model

# =========================
# LOAD MODEL
# =========================

model = load_model("model/music_model.keras")

# =========================
# READ MIDI DATA AGAIN
# =========================

notes = []

dataset_path = "midi_dataset"

for file in os.listdir(dataset_path):

    if file.endswith(".mid"):

        midi = converter.parse(
            os.path.join(dataset_path, file)
        )

        try:
            parts = instrument.partitionByInstrument(midi)

            if parts:
                notes_to_parse = parts.parts[0].recurse()
            else:
                notes_to_parse = midi.flat.notes

        except:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:

            if isinstance(element, note.Note):
                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):
                notes.append(
                    '.'.join(
                        str(n)
                        for n in element.normalOrder
                    )
                )

# =========================
# CREATE MAPPINGS
# =========================

pitchnames = sorted(set(notes))

note_to_int = dict(
    (note_name, number)
    for number, note_name in enumerate(pitchnames)
)

int_to_note = dict(
    (number, note_name)
    for number, note_name in enumerate(pitchnames)
)

# =========================
# START PATTERN
# =========================

sequence_length = 50

network_input = []

for i in range(len(notes) - sequence_length):

    seq_in = notes[i:i + sequence_length]

    network_input.append(
        [note_to_int[n] for n in seq_in]
    )

start = np.random.randint(
    0,
    len(network_input) - 1
)

pattern = network_input[start]

# =========================
# GENERATE NOTES
# =========================

prediction_output = []

for note_index in range(200):

    prediction_input = np.reshape(
        pattern,
        (1, len(pattern), 1)
    )

    prediction_input = prediction_input / float(
        len(pitchnames)
    )

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)

    pattern = pattern[1:]

print("Generated Notes:", len(prediction_output))

# =========================
# CONVERT TO MIDI
# =========================

offset = 0
output_notes = []

for pattern in prediction_output:

    if '.' in pattern:

        notes_in_chord = pattern.split('.')

        chord_notes = []

        for current_note in notes_in_chord:

            new_note = note.Note(int(current_note))

            new_note.storedInstrument = instrument.Piano()

            chord_notes.append(new_note)

        new_chord = chord.Chord(chord_notes)

        new_chord.offset = offset

        output_notes.append(new_chord)

    else:

        new_note = note.Note(pattern)

        new_note.offset = offset

        new_note.storedInstrument = instrument.Piano()

        output_notes.append(new_note)

    offset += 0.5

# =========================
# SAVE MIDI
# =========================

os.makedirs(
    "output",
    exist_ok=True
)

midi_stream = stream.Stream(output_notes)

midi_stream.write(
    'midi',
    fp='output/generated_music.mid'
)

print(
    "Music Saved: output/generated_music.mid"
)