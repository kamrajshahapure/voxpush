import speech_recognition as sr
import keyboard
import subprocess
import os
from datetime import datetime, timedelta
from vosk import Model, KaldiRecognizer
import json
import pyaudio

# Set the root directory for your code repositories
ROOT_DIR = '/path/to/project/where/git/repos/are/'

MODEL_PATH = "vosk-model-small-en-in-0.4/"
model = Model(MODEL_PATH)

# Function to find the most recently modified directory
def find_recently_modified_directory(root_dir):
    latest_time = datetime.min
    latest_dir = None
    for dirname in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, dirname)
        if os.path.isdir(subdir_path):  # Make sure it's a directory
            # List all files in the subdirectory
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)
                if os.path.isfile(file_path):  # Make sure it's a file
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mtime > latest_time:
                        latest_time = mtime
                        latest_dir = subdir_path
    return latest_dir

# Function to execute a command in the most recently modified directory
def execute_command(command):
    recent_dir = find_recently_modified_directory(ROOT_DIR)
    if recent_dir:
        if ("commit" in command) and ("push" in command):
            print(f"Executing command in {recent_dir}")
            
            branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=recent_dir,
            text=True).strip()
            
            subprocess.run('git add .', shell=True, cwd=recent_dir)
            subprocess.run('git commit -m "Pushed from speech to text app"', shell=True, cwd=recent_dir)
            subprocess.run('git push origin '+branch, shell=True, cwd=recent_dir)
    else:
        print("No recently modified directories found.")

# Function to start listening for speech and return the recognized text
def listen_for_speech():
    # Create a recognizer with the given model
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the microphone stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)

    stream.start_stream()

    print("Listening...")

    # Process audio in chunks
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

    # Parse the recognizer result
    try:
        result = json.loads(recognizer.Result())
        p = result['text']

        print(f"Recognized: {p}")
        return p
    except KeyError:
        print("Vosk could not understand audio")
    except Exception as e:
        print(f"Could not request results from Vosk service; {e}")

# Main function to handle hotkey press and speech recognition
def main():
    print("Press and hold '`' to start speech recognition.")
    while True:
        try:
            if keyboard.is_pressed('`'):
                text = listen_for_speech()
                if text:
                    execute_command(text)
                while keyboard.is_pressed('`'):
                    pass  # Wait until the hotkey is released
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()