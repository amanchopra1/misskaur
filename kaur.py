import openai
import speech_recognition as sr
from gtts import gTTS
import pygame
import os

# Set your OpenAI GPT-3 API key
api_key = "api"

# Initialize the OpenAI API client
openai.api_key = api_key

def chat_with_bot(prompt):
    # Make a request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].text.strip()

initial_prompt = "You are chatting with a humble 22-year-old female. She responds kindly and genuinely. Feel free to start the conversation."

print(initial_prompt)

pygame.mixer.init()  # Initialize pygame.mixer

recognizer = sr.Recognizer()

while True:
    print("Listening...")
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio).lower()
            print("You:", user_input)
        except sr.WaitTimeoutError:
            print("No input detected. Please speak.")
            continue
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            continue

    if user_input in ["bye", "goodbye", "exit"]:
        bot_response = "It was lovely chatting with you! Take care!"
        print("Bot:", bot_response)
        tts = gTTS(text=bot_response, lang="en", slow=False)
        tts.save("bot_response.mp3")
        
        pygame.mixer.music.load("bot_response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        
        os.remove("bot_response.mp3")
        break

    # Generate a response from the bot
    bot_response = chat_with_bot(user_input)
    print("Bot:", bot_response)

    tts = gTTS(text=bot_response, lang="en", slow=False)
    tts.save("bot_response.mp3")
    
    pygame.mixer.music.load("bot_response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    
    os.remove("bot_response.mp3")
