import json
import requests
import io
import os
import base64
import sys
from pathlib import Path
from PIL import Image, PngImagePlugin

from helper.settings_parser import read_yaml, load_prompts
from request import video_request

class ImageGenerator:
    def __init__(self, settings = None, output_path=Path('generated_images/')):
        self.settings = read_yaml(file_path='settings/config.yaml')
        self.api_url = self.settings['APP']['api_url']
        self.steps = self.settings['APP']['sampling_steps']
        self.prompts = self.settings['APP']['path_prompt_txt']
        self.output_path = self.settings['APP']['path_images']

    def load_arguments(self, argv):
        """
        Loads the prompt arguments from the command line.
        """
        return argv

    def generate_images(self, file):
        """
        Loads a json file from the specified directory and generates all included prompts.
        """
        prompts = load_prompts(path=file)
        counter=0
        for i in prompts['prompts']:
            counter+=1
            self.generate_image(prompt=i.get('prompt'), iter=counter)

    def generate_image(self, prompt, iter=0):
        """
        Generates an image with help of the specified prompt.
        The iteration parameter can be used to save the image with a unique name.
        """
        payload = {
            "prompt": f'{prompt}',
            "steps": self.steps
            }

        # send request to server
        response = requests.post(url=f'{self.api_url}/sdapi/v1/txt2img', json=payload)

        r = response.json()

        for i in r['images']:
            # decode image
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))     
            
            metadata = self.request_metadata(image=image, i=i)

            # save image with metadata
            pngInfo = PngImagePlugin.PngInfo()
            pngInfo.add_text("parameters", metadata)

            if iter != 0:
                image.save(f'{self.output_path}/{iter}.png', pnginfo=pngInfo)
            else: 
                image.save(f'{self.output_path}/output.png', pnginfo=pngInfo)

    def generate_video(self, prompt='', iter=0):
        """
        Generates an video with help of the specified prompt.
        The iteration parameter can be used to save the video with a unique name.
        """
        headers = {"Content-Type": "application/json; charset=utf-8"}

        payload = load_prompts('struct/video.json')

        #payload = video_request(prompt=prompt)

        # send request to server
        response = requests.post(url=f'{self.api_url}/run/predict', headers=headers, json=payload)

        r = response.json()

        # TODO Check for alternative method to retrieve images from response
        # for i in r['images']:
        #     # decode image
        #     image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))     
            
        #     metadata = self.request_metadata(image=image, i=i)

        #     # save image with metadata
        #     pngInfo = PngImagePlugin.PngInfo()
        #     pngInfo.add_text("parameters", metadata)

        #     if iter != 0:
        #         image.save(f'{self.output_path}/{iter}.png', pnginfo=pngInfo)
        #     else: 
        #         image.save(f'{self.output_path}/output.png', pnginfo=pngInfo)

    def request_metadata(self, image, i):
        """
        Gets the metadata of an image from the stable diffusion webui.
        """
        png_payload = {
            "image": "data:image/png;base64," + i
            }
        response = requests.post(url=f'{self.api_url}/sdapi/v1/png-info', json=png_payload)
        return response.json().get("info")

    def read_metadata(self, imagePath):
        """
        Reads the metadata of an specified image directly.
        """
        image = Image.open(imagePath)
        return image.text

if __name__ == "__main__":
    txt2img = ImageGenerator()
    prompt = txt2img.load_arguments(argv=sys.argv[1:])
    txt2img.generate_video(prompt)
