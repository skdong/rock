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
        response = self._client.recv(4096000)
        import pdb; pdb.set_trace()
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


def test_list_dbs():
    ovsdb_client = OvsdbClient()
    ovsdb_client.list_databases()

def test_delete_ucast():
    ovsdb_client = OvsdbClient()

    uuids = """321e7e68-54f4-4ff9-8c4a-44c97fd39b37
    46f68c87-4062-49b0-b520-7edcaa7d1c83
    5c651476-3900-4d44-9d9d-c0562738dea7
    65867c7c-d38b-441f-90fa-039d3ce16a67
    a435936d-2a0a-49d6-8efc-a1e5444b8e4a
    ad244d40-c80b-45d3-be0b-2c02bbe118d0
    bd6cfc2f-2bec-4839-9502-98583357265b
    c78ea4c2-03e8-425e-872f-6e3b638bb8b3
    c867dbb9-07e7-468e-849e-f1b444da9a20
    d79ea99d-d1b9-4e35-88d8-02bd81c83a24
    d994fb8b-c6ce-4643-9358-ed0314b7654a
    e3ac4c90-8935-4cbe-9884-d5d6a2cdd67d""".split()

    for uuid in uuids:
        #print uuid
        ovsdb_client.del_ucast_macs_remote(uuid)

def test_list_ucast():
    ovsdb_client = OvsdbClient()
    req = ovsdb_client.list_ucast_macs_remote()
    print json.loads(req)




