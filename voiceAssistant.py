import openai
import pyttsx3
import speech_recognition as sr
import time
import py_compile
import pyaudio

#set API Key!!!!!!
openai.api_key = "YOUR_API_KEY_HERE"

#initalize the text-to-speech
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Unknown Error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        temperature=0.8,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.getProperty('rate')
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Genius' to start recording")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    #record
                    filename = "input.wav"
                    print("Start speaking to genius")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    #Transcribe the audio
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        #Generate respone using Chat GPT
                        response = generate_response(text)
                        print(f"GPT says: {response}")

                        #read response
                        speak_text(response)
            except Exception as e:
                print("an error occurred: {}".format(e))

if __name__ == "__main__":
    main()
