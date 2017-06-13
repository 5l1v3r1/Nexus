from flask import Flask, jsonify, request, abort
from pylon import Pylon

pylon = Pylon("http://localhost:5000")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def client_post():
    if not (request.json and "action" in request.json):
        abort(400)

    if request.json["action"] == "register":
        print("Register Request Received")

        reply = pylon.register(request.remote_addr)
        # # Get remote address
        # address = request.remote_addr
        #
        # # Register probe with Nexus
        # nexus_reply = pylon.register(address)
        #
        # # Create return payload
        # reply = nexus_reply

        return jsonify(reply)

    if request.json["action"] == "beacon":
        print("Beacon Received From %s" % request.remote_addr)
        client_id = request.json["client_id"]

        nexus_reply = pylon.beacon(client_id, request.json)
        return jsonify(nexus_reply)

app.run(port=9999)
