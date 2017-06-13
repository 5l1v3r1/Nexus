import requests
import time
import json
import subprocess


PYLON_URL = "http://localhost:9999"


class Probe:
    pylons = []
    beacon_data = []
    client_id = None

    beacon_sleep_time = 5  # Time between beacons in seconds

    def __init__(self):
        pass

    def add_pylon(self, address, cm):
        self.pylons.append({"address": address,
                            "cm": cm})

    def nexus_register(self):
        """
        Register with Nexus server. Sets object's client_id.
        :return: client_id
        """
        pylon = self.pylons[0]  # Temporary hard code. Ideally this would pick a random valid pylon.

        if pylon["cm"] == "http":
            return self._http_nexus_register()

    def nexus_beacon(self):
        """
        Polls the nexus. Sends any beacon_data that needs to be sent to Nexus, and receives data from the server.
        :param data: {}
        :return:
        """

        pylon = self.pylons[0]  # Temporary hard code. Ideally this would pick a random valid pylon.

        if pylon["cm"] == "http":
            return self._http_nexus_beacon()

    def _http_nexus_register(self):
        r = requests.post(PYLON_URL, json={"action": "register"})
        if r.status_code == 200:
            r_client_id = json.loads(r.text)["client_id"]
            self.client_id = r_client_id
            return self.client_id
        else:
            print("Error registering")
            return None

    def _http_nexus_beacon(self):
        payload = {"client_id": self.client_id,
                   "data": self.beacon_data,
                   "action": "beacon"}

        r = requests.post(PYLON_URL, json=payload)

        if r.status_code == 200:  # Data successfully sent, so wipe it
            self.beacon_data = []

        print(r.text)


def do_command(command):
    output = subprocess.Popen(command, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
    return output.stdout.read() + output.stderr.read()


if __name__ == "__main__":
    probe = Probe()
    probe.add_pylon("http://localhost:9999/", "http")
    probe.nexus_register()
    print("Client ID: %s" % probe.client_id)

    while True:
        probe.nexus_beacon()
        time.sleep(probe.beacon_sleep_time)
