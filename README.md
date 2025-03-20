# Dataset Generator Helper

A tool designed for sign language recognition using machine learning.

## Overview

This project consists of three main modules:
1. Dataset Generator: Creates and manages sign language gesture datasets
2. Model Trainer: Trains machine learning models for sign language recognition
3. Recognition Module: Deploys trained models for real-time sign language interpretation

## Requirements

- Python 
- Poetry (for managing dependencies)

## Usage

### Dataset Generator Helper

1. Install dependencies :

```bash
poetry install
```

2. Run the tool :

```bash
poetry run python ./dataset_generator_helper/main.py
```

## Inspiration

 - Hand Tracking using MediaPipe from Sousannah (see [https://github.com/Sousannah/hand-tracking-using-mediapipe](https://github.com/Sousannah/hand-tracking-using-mediapipe))
 - Adding a Webcam Stream to our Python - Tkinter Drone Controller | Part 2: GUI Video Stream (see [https://www.youtube.com/watch?v=Dj-Jyws6rzA](https://www.youtube.com/watch?v=Dj-Jyws6rzA))
 - [Mudra signs](https://naruto.fandom.com/fr/wiki/Mudr%C3%A2) in Naruto

## License

This project is licensed under the GNU GPLv3 License - see the LICENSE file for details.