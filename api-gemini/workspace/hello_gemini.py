#!/usr/local/bin/python3

import os
import textwrap

import google.generativeai as genai
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


if __name__=="__main__":
    genai.configure(api_key=os.environ['API_KEY'])

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content('What is the meaning of life?', stream=True)
    for chunk in response:
       print(chunk.text)

    to_markdown(response.text)
