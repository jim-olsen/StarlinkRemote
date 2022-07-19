from flask import Flask, send_from_directory
import random
import json
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


@app.route("/starlink/status")
def starlink_status():
    status = dishy.get_status()

    return json.dumps(status, indent=3)


@app.route("/starlink/history")
def starlink_history():
    history = dishy.get_history();
    return json.dumps(history, indent=3)


if __name__ == "__main__":
    app.run(port=9999, debug=True)
