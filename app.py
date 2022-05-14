import os
import random
import re
import time

import openai

from flask import Flask
from flask import request

app = Flask(__name__)

# set api key. keep the key file hidden from public github repos etc
openai.api_key_path = "./key.txt"

prompt = "A man has a book, a chair, a pencil and a box. Written in the style of an action-packed performance, what does he do?"
# next = ["\n", "\nNext ", "\nNext, ", "\nAfterwards ", "\nAfterwards, ", "\nThen ",
#         "\nThen, "]  # possible next sequences to prompt gpt3
# script = [prompt + next[0]]  # start the script with the prompt and a newline

script = [prompt]

filename = "scripts/" + str(int(time.time())) + ".txt"


def script_as_str():
    return ' '.join(script)


def script_as_html():
    return "<p>" + '<br>'.join(script) + "</p>"


def write_response_to_file(response):
    with open(filename, 'a') as file:
        file.write(str(response))


@app.route("/")
def main():
    prompt = script_as_str() + request.args.get('prompt')
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=512,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0.5
    )
    text = gpt_response["choices"][0]["text"]
    text_no_whitespace = re.sub(r"\W", "", text)

    script.append(gpt_response["choices"][0]["text"])
    print(gpt_response["choices"][0]["text"])

    response = {
        "prompt": prompt,
        "script-html": script_as_html(),
        "time": time.time(),
        "response": gpt_response["choices"][0]["text"]
    }

    write_response_to_file(response)

    return response  # send the user the whole generated script
