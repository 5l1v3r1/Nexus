import requests


class Pylon:
    def __init__(self, nexus_address):
        self.nexus = nexus_address

    def register(self, probe_address):
        """
        Registers probe with Nexus
        :return: (int) probe's client id
        """
        data = {
            "address": probe_address
        }

        r = requests.post(self.nexus + "/register", json=data)

        return r.json()

    def beacon(self, client_id, data=None):
        r = requests.post(self.nexus + "/client/%s/beacon" % client_id, json=data)
        return r.json()



