from flask import Flask, send_from_directory, send_file
import random
import json
import io
import numpy as np
from PIL import Image
from Starlink import Starlink

app = Flask(__name__)
dishy = Starlink()


#
# Serve up the svelte application
#
@app.route("/")
def base():
    return send_from_directory('../svelte/public', 'index.html')


#
# Handle generic svelte application requests
#
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../svelte/public', path)


#
# provide the generic dishy status data through REST
#
@app.route("/starlink/status/")
def starlink_status():
    status = dishy.get_status()

    return json.dumps(status, indent=3)


#
# provide the dishy historical data through REST
#
@app.route("/starlink/history/")
def starlink_history():
    history = dishy.get_history()
    return json.dumps(history, indent=3)


#
# Get the obstruction image data, and transform into a png file and return through the get request
#
@app.route("/starlink/obstruction_image/")
def starlink_obstruction_image():
    obstruction_image = dishy.get_obstruction_map()
    numpy_image = np.array(obstruction_image).astype('uint8')
    img = Image.fromarray(numpy_image)
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


#
# Issue a request to the disk to stow itself
#
@app.route("/starlink/stow", methods=['POST'])
def stow_dish():
    dishy.dish_stow()


#
# Issue a request to the dish to unstow itself
#
@app.route("/starlink/unstow", methods=['POST'])
def unstow_dish():
    dishy.dish_unstow()


#
# Issue a request for the dish to reboot itself
#
@app.route("/starlink/reboot", methods=['POST'])
def reboot_dish():
    dishy.dish_reboot()


#
# Startup the flask server on port 9999.  Change the port here if you want it listening somewhere else, and simply
# execute this python file to startup your server and serve the svelte app
#
if __name__ == "__main__":
    app.run(port=9999, debug=True)
