from flask import Flask, send_from_directory, send_file
import random
import json
import io
import numpy as np
from PIL import Image
from Starlink import Starlink

app = Flask(__name__)
dishy = Starlink()


@app.route("/")
def base():
    return send_from_directory('../svelte/public', 'index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('../svelte/public', path)


@app.route("/hello")
def hello():
    return "<html><body><h1>Hello!</h1></body></html>"


@app.route("/rand")
def random_number():
    return str(random.randint(0, 100))


@app.route("/starlink/status/")
def starlink_status():
    status = dishy.get_status()

    return json.dumps(status, indent=3)


@app.route("/starlink/history/")
def starlink_history():
    history = dishy.get_history()
    return json.dumps(history, indent=3)


@app.route("/starlink/obstruction_image/")
def starlink_obstruction_image():
    obstruction_image = dishy.get_obstruction_map()
    numpy_image = np.array(obstruction_image).astype('uint8')
    img = Image.fromarray(numpy_image)
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


if __name__ == "__main__":
    app.run(port=9999, debug=True)
