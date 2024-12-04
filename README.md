# Audio Feature Extraction and Analysis Tool

A Python-based tool that processes audio files to extract various features such as BPM (tempo), key, genres, and, if applicable, transcribes vocals to analyze sentiment and subject matter. The results are compiled into a CSV file for easy analysis.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Environment Setup](#environment-setup)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Setup Guide](#step-by-step-setup-guide)
    - [1. Install Python](#1-install-python)
    - [2. Create a Virtual Environment (Optional but Recommended)](#2-create-a-virtual-environment-optional-but-recommended)
    - [3. Upgrade pip](#3-upgrade-pip)
    - [4. Install Required Python Packages](#4-install-required-python-packages)
    - [5. Download Additional NLTK Data](#5-download-additional-nltk-data)
    - [6. Install Pocketsphinx](#6-install-pocketsphinx)
    - [7. Install FFmpeg](#7-install-ffmpeg)
    - [8. Configure NLTK Data Path (If Necessary)](#8-configure-nltk-data-path-if-necessary)
- [Usage](#usage)
  - [1. Prepare Your Audio Files](#1-prepare-your-audio-files)
  - [2. Update Directory Paths in the Script](#2-update-directory-paths-in-the-script)
  - [3. Run the Script](#3-run-the-script)
  - [4. View the Results](#4-view-the-results)
- [Sample Output](#sample-output)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This tool automates the analysis of audio files by extracting musical features and textual information from vocals. It's particularly useful for music data analysis, music information retrieval tasks, and sentiment analysis of song lyrics.

## Features

- **BPM and Key Extraction:** Uses [Librosa](https://librosa.org/) to extract tempo and key information.
- **Genre Classification:** Identifies genres using [Musicnn](https://github.com/jordipons/musicnn).
- **Vocals Transcription:** Transcribes vocals using [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) with Pocketsphinx (offline).
- **Sentiment and Subject Matter Analysis:** Analyzes transcribed text using [NLTK](https://www.nltk.org/).
- **Batch Processing:** Processes both vocal and non-vocal tracks efficiently.
- **Output:** Saves results to a CSV file (`audio_analysis_results.csv`) for easy access and analysis.

## Environment Setup

Setting up the environment correctly is crucial for the smooth running of this tool. Follow the step-by-step guide below to set up your environment on a Windows machine.

### Prerequisites

- **Operating System:** Windows 10 or higher
- **Python:** Version 3.6 or higher
- **Git:** For cloning the repository

### Step-by-Step Setup Guide

#### 1. Install Python

Ensure Python 3.6 or higher is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

After installation, verify the installation by running:

```bash
python --version
```

#### 2. Create a Virtual Environment (Optional but Recommended)

It's good practice to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Command Prompt:**

  ```bash
  venv\Scripts\activate
  ```

- **PowerShell:**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

#### 3. Upgrade pip

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

#### 4. Install Required Python Packages

Create a `requirements.txt` file with the following content:

```plaintext
librosa
musicnn
SpeechRecognition
pocketsphinx
nltk
pandas
pydub
numpy
tqdm
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

#### 5. Download Additional NLTK Data

The script requires specific NLTK datasets. Run the following Python commands:

```python
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('popular')
```

Alternatively, you can run the script once, and it will download the necessary NLTK data automatically.

#### 6. Install Pocketsphinx

Pocketsphinx is required for offline speech recognition.

**Download and Install Pocketsphinx Binaries:**

Download the Pocketsphinx Windows installer from the [official website](https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/).

Run the installer and follow the on-screen instructions.

**Add Pocketsphinx to System PATH:**

After installation, add the Pocketsphinx installation directory to your system PATH.

1. Press `Win + X` and select **System**.
2. Click on **Advanced system settings**.
3. Click on **Environment Variables**.
4. Under **System variables**, find and select the **Path** variable, then click **Edit**.
5. Click **New** and add the path to the Pocketsphinx `bin` directory (e.g., `C:\Program Files\Pocketsphinx\bin`).
6. Click **OK** to close all dialog boxes.

**Verify Installation:**

Open Command Prompt and run:

```bash
pocketsphinx_continuous -h
```

You should see the help information for Pocketsphinx.

#### 7. Install FFmpeg

`pydub` relies on FFmpeg for audio processing.

**Download FFmpeg:**

Download the latest FFmpeg build from the [official website](https://ffmpeg.org/download.html).

**Extract and Add to PATH:**

Extract the downloaded zip file and add the `bin` directory to your system PATH following the same steps as above.

**Verify Installation:**

Open Command Prompt and run:

```bash
ffmpeg -version
```

You should see FFmpeg version information.

#### 8. Configure NLTK Data Path (If Necessary)

The script sets the NLTK data path to `C:\Users\USERNAME\AppData\Roaming\nltk_data`. If your NLTK data is located elsewhere, update the path in the script accordingly:

```python
nltk.data.path.append(r'C:\Path\To\Your\nltk_data')
```

## Usage

### 1. Prepare Your Audio Files

- **With Vocals:** Place audio files **with vocals** in the `vocals` directory.
- **Without Vocals:** Place audio files **without vocals** in the `novocals` directory.

Ensure the directory structure is as follows:

```plaintext
your-repo-name/
├── vocals/
│   └── Vocals/
│       ├── song1.mp3
│       ├── song2.wav
│       └── ...
├── novocals/
│   ├── instrumental1.mp3
│   ├── instrumental2.wav
│   └── ...
├── audio_feature_extractor.py
├── requirements.txt
└── README.md
```

### 2. Update Directory Paths in the Script

Open `audio_feature_extractor.py` and update the following lines to match your directory structure:

```python
vocals_dir = r'C:\Path\To\Your\Vocals'
novocals_dir = r'C:\Path\To\Your\Novocals'
```

### 3. Run the Script

Execute the script using Python:

```bash
python audio_feature_extractor.py
```

The script will process all audio files in the specified directories and generate an `audio_analysis_results.csv` file in the root directory.

### 4. View the Results

Open `audio_analysis_results.csv` using Excel, Google Sheets, or any CSV viewer to analyze the extracted data.

## Sample Output

I have uploaded a sample output CSV file.
Below is a sample of the output CSV file:

| file_name               | file_path                                                      | bpm       | key        | genres                                      | genre_confidence_scores                                   | sentiment                                      | subject_matter | transcribed_text                                                                                                                            |
|-------------------------|----------------------------------------------------------------|-----------|------------|---------------------------------------------|------------------------------------------------------------|------------------------------------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| A Beacon of Hope.mp3    | c:\Python39\audiodetect\vocals\Vocals\A Beacon of Hope.mp3     | 95.703125 | D major    | ['guitar', 'vocal', 'female', 'singing', 'slow'] | [0.5092698, 0.3233298, 0.25438255, 0.24055085, 0.21358222] | {'neg': 0.082, 'neu': 0.726, 'pos': 0.193, 'compound': 0.9246} | ['love']       | in this bodes no walls are made moves very thin man needs how's the food in with ms lewis moves inland...                                 |
| A Christmas Eve Tale.mp3 | c:\Python39\audiodetect\vocals\Vocals\A Christmas Eve Tale.mp3 | 135.9991776 | G major    | ['guitar', 'male', 'vocal', 'man']           | [0.20566337, 0.1769308, 0.1646796, 0.15528043, 0.15339182] | {'neg': 0.082, 'neu': 0.828, 'pos': 0.09, 'compound': 0.4983}  | []             | on it and whispers of of of the adult and nobody out of the lives of women have an mole now why when...                                       |
| A Dance in the Snow.wav | c:\Python39\audiodetect\vocals\Vocals\A Dance in the Snow.wav | 103.359375 | G# major   | ['female', 'woman', 'vocal', 'female vocal', 'singing'] | [0.47164688, 0.34162813, 0.3385164, 0.254514, 0.23821594] | {'neg': 0.082, 'neu': 0.834, 'pos': 0.085, 'compound': 0.3612} | ['work']       | it says her par les against me in my view his knee in lanni it's noise you see it in hot day it was high...                                 |
| ...                     | ...                                                            | ...       | ...        | ...                                         | ...                                                        | ...                                            | ...            | ...                                                                                                                                          |

## Dependencies

- **Python 3.6 or Higher**

- **Python Libraries:**
  - [Librosa](https://librosa.org/)
  - [Musicnn](https://github.com/jordipons/musicnn)
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
  - [Pocketsphinx](https://github.com/cmusphinx/pocketsphinx)
  - [NLTK](https://www.nltk.org/)
  - [Pydub](https://github.com/jiaaro/pydub)
  - [NumPy](https://numpy.org/)
  - [Pandas](https://pandas.pydata.org/)
  - [Tqdm](https://tqdm.github.io/)

## Configuration

- **NLTK Data Path:**

  Ensure the `nltk_data` path in the script matches your NLTK installation. If your NLTK data is located in a different directory, update the following line in `audio_feature_extractor.py`:

  ```python
  nltk.data.path.append(r'C:\Path\To\Your\nltk_data')
  ```

- **Audio Directories:**

  Update the `vocals_dir` and `novocals_dir` variables in the script to point to your audio file directories:

  ```python
  vocals_dir = r'C:\Path\To\Your\Vocals'
  novocals_dir = r'C:\Path\To\Your\Novocals'
  ```

## Troubleshooting

- **Pocketsphinx Not Found:**

  Ensure Pocketsphinx is installed correctly and its `bin` directory is added to the system PATH. Verify by running `pocketsphinx_continuous -h` in Command Prompt.

- **FFmpeg Issues:**

  If you encounter issues related to audio processing, ensure FFmpeg is installed and added to the system PATH. Verify by running `ffmpeg -version` in Command Prompt.

- **NLTK Data Errors:**

  If the script cannot find NLTK data, ensure the `nltk_data` path is correctly set in the script and that the necessary datasets are downloaded.

- **Permission Issues:**

  Run Command Prompt or PowerShell as an administrator if you encounter permission-related errors during installation.

- **Audio File Errors:**

  Ensure your audio files are not corrupted and are in supported formats (`.wav`, `.mp3`, `.flac`, `.m4a`, `.aac`, `.ogg`).

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Describe your changes and submit the pull request for review.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Happy Coding! 🎵*
```
