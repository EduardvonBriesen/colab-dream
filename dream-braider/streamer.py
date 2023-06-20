from flask import Flask, Response, request
import os
import time

# from pyngrok import ngrok

app = Flask(__name__)
stream = None

# public_url = ngrok.connect(5000).public_url
# print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 5000))

path = '/home/ubuntu/stable-diffusion-webui/outputs/img2img-images/dream/'

def gen():
    i = 0

    # 
    processed_images = []

    while True:
        images = get_all_images()

        unprocessed_images = [img for img in images if img not in processed_images]

        unprocessed_images_len = len(unprocessed_images) #- i

        # Buffer which is used to slow down the slideshow
        buffer = max(0.125, 1 - unprocessed_images_len * 0.008)
        print("Image count: ", len(images), "Unprocessed images: ", unprocessed_images_len, "; Buffer: ", buffer)
        
        time.sleep(buffer)

        # Check if images are available
        if unprocessed_images:
            image_name = unprocessed_images[0]
            im = open(path + image_name, 'rb').read()
            processed_images.append(image_name)
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

# @app.route('/')
# def index():
#     return "<html><head><img src='/slideshow' style='width: 90%; height: 90%;'/>" \
#            "</body></html>"

@app.route('/')
def index():
    return """
        <html>
            <head>
                <style>
                    /* Set background color to black */
                    body {
                        background-color: black;
                        margin: 0;
                    }
                    /* Center the slideshow */
                    #slideshow {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        width: 90%;
                        height: 90%;
                    }
                </style>
            </head>
            <body>
                <img id="slideshow" src="/slideshow" />
            </body>
        </html>
    """

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