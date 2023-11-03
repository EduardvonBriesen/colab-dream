import os
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

# Define the path to the directory where videos are located
video_directory = '/workspace/stable-diffusion-webui/outputs/img2img-images/dream/'

def get_video_files(directory):
    video_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.mp4')]
    sorted_videos = sorted(video_files, key=lambda x: os.path.getctime(x))
    return sorted_videos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_list')
def get_video_list():
    video_files = get_video_files(video_directory)
    return jsonify(video_files)

def generate():
    video_files = get_video_files(video_directory)
    for video_file in video_files:
        with open(video_file, 'rb') as video:
            print(video_file)
            while True:
                chunk = video.read(512)
                if not chunk:
                    break
                yield chunk

@app.route('/video')
def video():
    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
