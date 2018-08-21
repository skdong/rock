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
        self._generate_client()

    def _generate_client(self):
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
        response = get_response(self._client)
        print response
        return response

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
                          "where": [["_uuid", "==", ["uuid", uuid]]]
                      },
                      {
                          "durable": True,
                          "op": "commit"
                      }
                      ]
            return self.run_operat(method, params)

    def list_table(self, table):
        if table:
            method = "transact"
            params = ["hardware_vtep",
                      {
                          "op": "select",
                          "table": table,
                          "where": []
                      },
                      ]
            return self.run_operat(method, params)

    def list_ucast_macs_remote(self):
        return self.list_table("Ucast_Macs_Remote")


def get_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((OVSDB_IP, OVSDB_PORT))
    return client


def get_response(client):
    response = ''
    if client and hasattr(client, 'recv'):
        buf = client.recv(BUFFER_SIZE)
        while buf:
            response += buf
            buf = client.recv(BUFFER_SIZE)
    return response



