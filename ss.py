import time
import pyttsx3
import openai
import speech_recognition as sr
from gtts import gTTS
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
def generate_response(prompt):
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

class VoiceAssistantUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create the label
        self.label = Label(text="Welcome to Voice Assistant", font_size=20)
        self.add_widget(self.label)

        # Create the text input
        self.text_input = TextInput(hint_text="Enter your command here", font_size=16)
        self.add_widget(self.text_input)

        # Create the button
        self.button = Button(text="Start Voice Assistant", font_size=16)
        self.button.bind(on_press=self.start_voice_assistant)
        self.add_widget(self.button)

        # Create the label for displaying responses
        self.response_label = Label(text="", font_size=16)
        self.add_widget(self.response_label)

    def start_voice_assistant(self, instance):
        user_input = self.text_input.text

        # Perform voice assistant actions with user input
        filename = 'input.wav'
        text = transcribe_audio_to_text(filename)
        if text:
            print(f"You said: {text}")
            response = generate_response(text)
            print(f"GPT-3 says: {response}")
            speak_text(response)

        # Update the response label with assistant's response
        self.response_label.text = response

        # Clear the text input
        self.text_input.text = ""


class VoiceAssistantApp(App):
    def build(self):
        return VoiceAssistantUI()


if __name__ == "__main__":
    VoiceAssistantApp().run()
