import os
import openai
import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import threading
import click
import torch
import numpy as np
import requests

openai.api_key = "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"
render_url = "https://localhost:8000/prompt"

dream_list = []
prompt_list = []


@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Whether to use English model", is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic engergy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--save_file", default=False, help="Flag to save file", is_flag=True, type=bool)
def main(model, english, verbose, energy, pause, dynamic_energy, save_file):
    temp_dir = tempfile.mkdtemp() if save_file else None
    # there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir)).start()
    threading.Thread(target=transcribe_forever,
                     args=(audio_queue, result_queue, audio_model, english, verbose, save_file)).start()

    while True:
        # print(result_queue.get())
        add_dream(result_queue.get())


def record_audio(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir):
    # load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        i = 0
        while True:
            # get and save audio to wav file
            audio = r.listen(source)
            if save_file:
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                filename = os.path.join(temp_dir, f"temp{i}.wav")
                audio_clip.export(filename, format="wav")
                audio_data = filename
            else:
                torch_audio = torch.from_numpy(np.frombuffer(
                    audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

            audio_queue.put_nowait(audio_data)
            i += 1


def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose, save_file):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        if not verbose:
            predicted_text = result["text"]
            result_queue.put_nowait("You said: " + predicted_text)
        else:
            result_queue.put_nowait(result)

        if save_file:
            os.remove(audio_data)


def add_dream(dream):
    dream_list.append(dream)
    print("Adding dream: " + dream)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_prompt(),
        temperature=1,
        max_tokens=100,
    )
    print("New prompt:" + response.choices[0].text)
    prompt_list.append(response.choices[0].text)
    send_dreams(response.choices[0].text)


def generate_prompt():
    # print("Generating prompt")
    # open text file in read mode
    # text_file = open("example_prompts.txt", "r")
    # text_file.close()

    return """Generate a new prompt with the phrases {}""".format(
        dream_list
    )


# Sends dream via rest api
def send_dreams(dream):
    response = requests.post(render_url, json={"prompt": dream})
    if response.status_code == 200:
        print("Dream sent successfully")
    else:
        print("Error sending dream")


main()

# def get_image(prompt):
#     base_url = "https://api.newnative.ai/stable-diffusion?prompt="

#     response = requests.request("GET", base_url + prompt)
#     data = response.json()
#     print(data["image_url"])


# print("Starting")
# while True:
#     input_text = ""
#     with sr.Microphone() as source:
#         print("Talk")
#         audio_text = r.listen(source)
#         print("Time over, thanks")

#         try:
#             # using google speech recognition
#             input_text = r.recognize_google(audio_text)
#             print("Text: "+input_text)
#         except:
#             print("Sorry, I did not get that")

#     add_dream(input_text)
