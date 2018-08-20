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
        if uuid:
            operations = {

            }
            self.run_operat(operations)


def get_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((OVSDB_IP, OVSDB_PORT))
    return client

ovsdb_client = OvsdbClient()
ovsdb_client.list_databases()
