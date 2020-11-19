import unittest
from server import app


class BridgeTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test01_creating_device_A1(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A1"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A1")

    def test02_creating_device_A2(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A2"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A2")

    def test03_creating_device_A3(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A3"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A3")

    def test04_adding_bridge_B1(self):
        call = self.app.post('/ajiranet/process',
                             data='''ADD BRIDGE B1 UPPER''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added B1")

    def test05_connect_A1_B1_A2(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                                     content-type : application/json

                                     {"source" : "B1", "targets" : ["A1","A2"]}''')
        # self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test05_connect_A2_A3(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                                     content-type : application/json

                                     {"source" : "A2", "targets" : ["A3"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test06_get_route_for_a1_a3(self):
        call = self.app.post('/ajiranet/process',
                             data='''FETCH /info-routes?from=A1&to=A3''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Route is A1->B1->A2->A3")

    def test07_send_message_from_a1_a3(self):
        call = self.app.post('/ajiranet/process',
                             data='''SEND /info?from=A1&to=A3&msg="hello"''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Message is \"HELLO\"")


if __name__ == '__main__':
    unittest.main()
