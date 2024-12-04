import os
import warnings
import librosa
import musicnn
import speech_recognition as sr
import nltk
nltk.data.path.append(r'C:\Users\hotra\AppData\Roaming\nltk_data')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import pandas as pd
from pydub import AudioSegment
import numpy as np
from tqdm import tqdm

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="librosa")
warnings.filterwarnings("ignore", category=UserWarning, module="musicnn")

# Download specific resources
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('popular')  # To include commonly used datasets

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Define Subject Matter Keywords
SUBJECTS = {
    "love": ["love", "heart", "romance"],
    "work": ["work", "job", "career"],
    "heart-ache": ["heartache", "sad", "broken"],
    "public-speaking": ["speech", "presentation", "public speaking"],
    "traveling in italy": ["travel", "italy", "trip"]
}

def get_audio_files(directory):
    audio_files = []
    for root, dirs, files in os.walk(directory):
        # Exclude the __MACOSX directory
        dirs[:] = [d for d in dirs if d != '__MACOSX']
        for file in files:
            # Skip files starting with '._' or hidden files
            if file.startswith('._') or file.startswith('.'):
                continue
            if file.lower().endswith(('.wav', '.mp3', '.flac', '.m4a', '.aac', '.ogg')):
                audio_files.append(os.path.join(root, file))
    return audio_files

def convert_to_wav(file_path):
    try:
        if not file_path.lower().endswith('.wav'):
            audio = AudioSegment.from_file(file_path)
            wav_path = file_path.rsplit('.', 1)[0] + '_temp.wav'
            audio.export(wav_path, format='wav')
            return wav_path
        else:
            return file_path
    except Exception as e:
        print(f"Error converting file to WAV format for {file_path}: {e}")
        return None

def extract_bpm_librosa(file_path):
    """
    Extract BPM using Librosa
    """
    try:
        y, sr = librosa.load(file_path)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo_librosa = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return tempo_librosa[0]
    except Exception as e:
        print(f"Error extracting BPM with Librosa for {file_path}: {e}")
        return None

def extract_key_librosa(file_path):
    """
    Extract Key using Librosa
    """
    try:
        y, sr = librosa.load(file_path)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = chroma.mean(axis=1)
        key_index = chroma_mean.argmax()
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                     'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_librosa = key_names[key_index % 12]
        return f"{key_librosa} major"
    except Exception as e:
        print(f"Error extracting Key with Librosa for {file_path}: {e}")
        return None

def extract_bpm_key(file_path):
    """
    Extract BPM and Key using Librosa
    """
    bpm = extract_bpm_librosa(file_path)
    key = extract_key_librosa(file_path)
    return bpm, key

def extract_genres(file_path):
    """
    Extract Genres using Musicnn
    """
    try:
        from musicnn import extractor
        taggram, tags = extractor.extractor(file_path, extract_features=False)
        avg_taggram = np.mean(taggram, axis=0)
        tag_scores = dict(zip(tags, avg_taggram))
        top_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
        return top_tags[:5]  # Return top 5 genres
    except Exception as e:
        print(f"Error extracting genres for {file_path}: {e}")
        return []

def transcribe_vocals(file_path):
    """
    Transcribe vocals using SpeechRecognition and pocketsphinx (offline)
    """
    try:
        recognizer = sr.Recognizer()

        # Convert to WAV if necessary
        if not file_path.lower().endswith('.wav'):
            audio = AudioSegment.from_file(file_path)
            temp_wav = file_path.rsplit('.', 1)[0] + '_transcribe_temp.wav'
            # Ensure the audio is in PCM format
            audio.export(temp_wav, format='wav', parameters=["-acodec", "pcm_s16le"])
            file_to_use = temp_wav
        else:
            file_to_use = file_path

        with sr.AudioFile(file_to_use) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_sphinx(audio_data)
            except sr.UnknownValueError:
                text = ""
            except sr.RequestError as e:
                print(f"Sphinx error; {e}")
                text = ""

        # Clean up temporary WAV file
        if file_to_use != file_path and os.path.exists(file_to_use):
            os.remove(file_to_use)

        return text
    except Exception as e:
        print(f"Error transcribing vocals for {file_path}: {e}")
        return ""

def analyze_text(text):
    """
    Analyze sentiment and subject matter of the transcribed text
    """
    try:
        sentiment = sia.polarity_scores(text)
        detected_subjects = []
        words = word_tokenize(text.lower())
        for subject, keywords in SUBJECTS.items():
            if any(keyword in words for keyword in keywords):
                detected_subjects.append(subject)
        return sentiment, detected_subjects
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return {}, []

def process_file(file_path, has_vocals):
    # Initialize result dictionary
    result = {
        'file_name': os.path.basename(file_path),
        'file_path': file_path,
        'bpm': None,
        'key': None,
        'genres': None,
        'genre_confidence_scores': None,
        'sentiment': None,
        'subject_matter': None,
        'transcribed_text': None,
    }

    # Convert to WAV if necessary
    wav_file = convert_to_wav(file_path)
    if wav_file is None:
        print(f"Failed to convert {file_path} to WAV. Skipping file.")
        return result

    # Extract BPM and Key
    bpm, key = extract_bpm_key(wav_file)
    result['bpm'] = bpm
    result['key'] = key

    # Extract Genres
    genres = extract_genres(wav_file)
    result['genres'] = [tag for tag, score in genres]
    result['genre_confidence_scores'] = [score for tag, score in genres]

    # If the file has vocals, transcribe and analyze text
    if has_vocals:
        text = transcribe_vocals(wav_file)
        result['transcribed_text'] = text
        sentiment, detected_subjects = analyze_text(text)
        result['sentiment'] = sentiment
        result['subject_matter'] = detected_subjects
    else:
        result['transcribed_text'] = None
        result['sentiment'] = None
        result['subject_matter'] = None

    # Clean up the temporary WAV file if it was created
    if wav_file != file_path and os.path.exists(wav_file):
        os.remove(wav_file)

    return result

def main():
    vocals_dir = r'c:\Python39\audiodetect\vocals\Vocals'
    novocals_dir = r'c:\Python39\audiodetect\novocals'

    vocals_files = get_audio_files(vocals_dir)
    novocals_files = get_audio_files(novocals_dir)

    all_results = []

    # Process vocals files
    for file_path in tqdm(vocals_files, desc="Processing vocals files"):
        result = process_file(file_path, has_vocals=True)
        all_results.append(result)

    # Process novocals files
    for file_path in tqdm(novocals_files, desc="Processing novocals files"):
        result = process_file(file_path, has_vocals=False)
        all_results.append(result)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('audio_analysis_results.csv', index=False)

if __name__ == '__main__':
    main()
