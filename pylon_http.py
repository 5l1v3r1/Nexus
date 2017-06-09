from flask import Flask, jsonify, request, abort
import requests

NEXUS_URL = "http://localhost:5000"

app = Flask(__name__)


@app.route("/", methods=["POST"])
def client_post():
    if not (request.json and "action" in request.json):
        abort(400)

    if request.json["action"] == "register":
        print("Register Request Received")
        data = request.json
        data["address"] = request.remote_addr
        r = requests.post(NEXUS_URL + "/register", json=request.json)
        return r.text

    if request.json["action"] == "heartbeat":
        print("Heartbeat Received From %s" % request.remote_addr)
        r = requests.post(NEXUS_URL + "/client/%s/heartbeat" % request.json["id"], json=request.json)
        return r.text


def client_get():
    pass

app.run(port=9999)
