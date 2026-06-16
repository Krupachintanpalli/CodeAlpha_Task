import os
import numpy as np

from music21 import converter, instrument, note, chord

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.utils import to_categorical

# =========================
# STEP 1: READ MIDI FILES
# =========================

notes = []

dataset_path = "midi_dataset"

for file in os.listdir(dataset_path):

    if file.endswith(".mid"):

        print("Reading:", file)

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

                notes.append(
                    str(element.pitch)
                )

            elif isinstance(element, chord.Chord):

                notes.append(
                    '.'.join(
                        str(n)
                        for n in element.normalOrder
                    )
                )

print("\nTotal notes extracted:", len(notes))
print("\nFirst 20 notes:")
print(notes[:20])

# =========================
# STEP 2: CREATE VOCABULARY
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

print("\nUnique notes:", len(pitchnames))

# =========================
# STEP 3: CREATE SEQUENCES
# =========================

sequence_length = 50

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):

    seq_in = notes[i:i + sequence_length]

    seq_out = notes[i + sequence_length]

    network_input.append(
        [note_to_int[n] for n in seq_in]
    )

    network_output.append(
        note_to_int[seq_out]
    )

print("Training patterns:", len(network_input))

# =========================
# STEP 4: PREPARE DATA
# =========================

n_patterns = len(network_input)

network_input = np.reshape(
    network_input,
    (n_patterns, sequence_length, 1)
)

network_input = network_input / float(
    len(pitchnames)
)

network_output = to_categorical(
    network_output
)

print("Input Shape:", network_input.shape)
print("Output Shape:", network_output.shape)

# =========================
# STEP 5: BUILD MODEL
# =========================

model = Sequential()

model.add(
    LSTM(
        256,
        input_shape=(
            network_input.shape[1],
            network_input.shape[2]
        ),
        return_sequences=True
    )
)

model.add(
    Dropout(0.3)
)

model.add(
    LSTM(256)
)

model.add(
    Dense(128)
)

model.add(
    Dropout(0.3)
)

model.add(
    Dense(
        network_output.shape[1],
        activation='softmax'
    )
)

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam'
)

print("\nModel Created Successfully")

# =========================
# STEP 6: TRAIN MODEL
# =========================

print("\nTraining Started...\n")

model.fit(
    network_input,
    network_output,
    epochs=3,
    batch_size=64
)

print("\nTraining Complete")

# =========================
# STEP 7: SAVE MODEL
# =========================

os.makedirs(
    "model",
    exist_ok=True
)

model.save(
    "model/music_model.keras"
)

print(
    "\nModel Saved Successfully"
)

print(
    "\nSaved at: model/music_model.keras"
)