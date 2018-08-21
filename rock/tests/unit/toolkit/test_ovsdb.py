import unittest
from rock.toolkit import ovsdb

class TestOvsdbClient(unittest.TestCase):
    def runTest(self):
        self._client = ovsdb.OvsdbClient()

    def test_list_databases(self):
        self._client.list_databases()

    def test_del_ucast_macs_remote(self):
        self._client.del_ucast_macs_remote()


