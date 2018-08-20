import sys
import socket
import json

from oslo_utils import uuidutils

OVSDB_IP = '9.9.9.5'
OVSDB_PORT = 6641
DEFAULT_DB = 'hardware_vtep'
BUFFER_SIZE = 4096


class OvsdbClient(object):
    """

    """

    def __init__(self):
        self._client = None

    def generate_client(self):
        self._client = get_client()

    def run_operat(self, method, params):
        """
        :param method:
        :param params:
        :return:
        """
        operations = {
            "method": method,
            "params": params,
            "id": uuidutils.generate_uuid()
        }
        self._client.send(json.dumps(operations))
        response = self._client.recv(4096)
        print response

    def list_databases(self):
        self.run_operat("list_dbs",
                        [])

    def del_ucast_macs_remote(self, uuid=None):
        """
        :param uuid:
        :return:
        """
        if uuid:
            method = "transact"
            params = ["hardware_vtep",
                      {
                          "op": "delete",
                          "table": "Ucast_Macs_Remote",
                          "where": [["_uuid", "==", uuid]]
                      },
                      {
                          "durable": True,
                          "op": "commit"
                      }
                      ]
            self.run_operat(method, params)


def get_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((OVSDB_IP, OVSDB_PORT))
    return client


ovsdb_client = OvsdbClient()
ovsdb_client.list_databases()

uuid = '1c2b0140-1478-4a25-a3a6-92b7b89fc60c'
ovsdb_client.del_ucast_macs_remote(uuid)
