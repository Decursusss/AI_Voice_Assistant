import time
import pyttsx3
import openai
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import wave

# Set up OpenAI API credentials
openai.api_key = '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'

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

# Function to translate text using OpenAI API
def generate_responce(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text


# Function to convert translated text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()


# Function to play audio using pyaudio
def main():
    while True:
        print("Say 'Jarvis' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == 'jarvis':
                    filename = 'input.wav'
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        responce = generate_responce(text)
                        print(f"GPT-3 says: {responce}")
                        speak_text(responce)
                elif transcription.lower() == 'stop':
                    quit()
            except Exception as e:
                print("An error occurred: {}".format(e))


# Run the voice translator app
if __name__ == "__main__":
    main()
