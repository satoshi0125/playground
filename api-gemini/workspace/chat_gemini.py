#!/usr/local/bin/python3

import os
import textwrap

import google.generativeai as genai
from hello_gemini import to_markdown


genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

running = True
while running:
    user_input = input("You: ")

    if user_input == "end" or user_input == "finish":
        print("Gemini: Good bye")
        running = False
    else:
        response = chat.send_message(user_input, stream=True)
        print("Gemini: ")
        for chunk in response:
            print(chunk.text)
