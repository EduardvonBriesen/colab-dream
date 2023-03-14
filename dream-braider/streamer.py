from flask import Flask, Response, request
import os
import time

app = Flask(__name__)
stream = None

path = 'C:/Repos/stable-diffusion-webui/outputs/img2img-images/dream/'

def gen():
    i = 0

    while True:
        images = get_all_images()

        # Buffer which is used to slow down the slideshow
        buffer = max(0.125, 1 - len(images) * 0.008)
        print("Buffer: ", buffer)
        
        time.sleep(buffer)

        # Check if images are available
        if images:
            image_name = images[i]
            im = open(path + image_name, 'rb').read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
            i += 1
            if i >= len(images):
                i = 0

def get_all_images():
    image_folder = path
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    return images

@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<html><head><img src='/slideshow' style='width: 90%; height: 90%;'/>" \
           "</body></html>"

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def app_run():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

def run():
    if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True, use_reloader=False)

run()