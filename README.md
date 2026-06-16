# CodeAlpha Music Generation with AI

## Overview

This project generates music using Artificial Intelligence and Deep Learning.

## Technologies Used

* Python
* TensorFlow
* Keras
* Music21
* NumPy

## Dataset

The model was trained on Beethoven MIDI files.

## Features

* Reads MIDI files
* Extracts musical notes and chords
* Trains an LSTM neural network
* Generates new music sequences
* Saves generated music as a MIDI file

## Project Structure

CodeAlpha_MusicGeneration/

* midi_dataset/
* model/
* output/
* train.py
* generate.py
* requirements.txt
* README.md

## How to Run

Install dependencies:

pip install -r requirements.txt

Train the model:

python train.py

Generate music:

python generate.py

Generated file:

output/generated_music.mid

## Output

The trained model generates new musical note sequences and stores them in MIDI format.
