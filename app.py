import os
import random
import re
import time

import openai

from flask import Flask

app = Flask(__name__)

# set api key. keep the key file hidden from public github repos etc
openai.api_key_path = "./key.txt"

prompt = "A man has a book, a chair, a pencil and a box. Written in the style of an action-packed performance, what does he do?"
next = ["\n", "\nNext ", "\nNext, ", "\nAfterwards ", "\nAfterwards, ", "\nThen ",
        "\nThen, "]  # possible next sequences to prompt gpt3
script = [prompt + next[0]]  # start the script with the prompt and a newline

filename = "scripts/" + str(int(time.time())) + ".txt"

def script_as_str():
    return ' '.join(script)


def script_as_html():
    return "<p>" + '<br>'.join(script) + "</p>"


def create_prompt():
    return script_as_str() + random.choice(next)

def write_script_to_file():
    with open(filename, 'w') as file:
        file.write(script_as_str())


@app.route("/")
def main():
    while True:
        prompt = create_prompt()
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=512,
            top_p=1,
            frequency_penalty=2,
            presence_penalty=0.5
        )
        text = response["choices"][0]["text"]
        text_no_whitespace = re.sub(r"\W", "", text)

        if len(text_no_whitespace) > 0:  # if the completion isn't blank
            break

    script.append(response["choices"][0]["text"])
    print(response["choices"][0]["text"])

    write_script_to_file()

    return script_as_html()  # send the user the whole generated script
