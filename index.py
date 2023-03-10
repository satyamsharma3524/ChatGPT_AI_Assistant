import openai
import pyttsx3
import speech_recognition as sr
import time

# set OpenAI API key
openai.api_key = "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"

# initiazlize the text-to-speech engine
engine = pyttsx3.init()
def transcribe_audio_to_text(filename):
    # initialize the recognizer
    r = sr.Recognizer()
    # open the microphone and start recording
    with sr.AudioFile(filename) as source:
        print("Say something!")
        audio = r.record(source)
    # recognize speech using Google Speech Recognition
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
def generate_response(prompt):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=4000,
      n=1,
      stop=None,
    )
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    print("Welcome to the OpenAI chatbot demo!")
    while True:
        print("say 'hello' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcrption = recognizer.recognize_google(audio)
                if transcrption.lower() == "hello":
                    filename = "audio.wav"
                    print("Say something!")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                            
                    # transcripbe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        # generate response using OpenAI GPT-3
                        response = generate_response(text)
                        print(f"Jarvis says: {response}")
                        
                        # read response using text-to-speech
                        speak_text(response)
                        
            except Exception as e:
                print(e)
                print("Say that again please...")
                
if __name__ == "__main__":
    main()