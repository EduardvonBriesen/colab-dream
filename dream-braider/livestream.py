import os
from flask import Flask, render_template, Response, jsonify, request

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

def generate_video(index):
    video_path = os.path.join(get_video_files(video_directory)[index])
    
    with open(video_path, 'rb') as video:
        while True:
            chunk = video.read(1024)
            if not chunk:
                break
            yield chunk

@app.route('/video_feed')
def video_feed():
    index = int(request.args.get('index', 0))
    return Response(generate_video(index), mimetype='video/mp4')

@app.route('/buffer_size')
def get_buffer_size():
    index = int(request.args.get('index', 0))
    remaining_videos = get_video_files(video_directory)
    if(index >= len(remaining_videos)):
        return jsonify(0)
    length = len(remaining_videos[index:])
    return jsonify(length)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)