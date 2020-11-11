import unittest
from server import app


class AjiraNetTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test01_creating_device_A1(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json
                             
                             {"type" : "COMPUTER", "name" : "A1"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"],"Successfully added A1")

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

    def test04_creating_device_with_wrong_syntax(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Invalid command syntax")

    def test05_creating_phone_device(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json
                             
                             {"type" : "PHONE", "name" : "A3"}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "type 'PHONE' is not supported")

    def test06_creating_A1_again(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A1"}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Device 'A1' already exists")

    def test07_creating_device_A4(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A4"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A4")

    def test08_creating_device_A5(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A5"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A5")

    def test09_creating_device_A6(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "COMPUTER", "name" : "A6"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added A6")

    def test10_creating_device_R1(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /devices
                             content-type : application/json

                             {"type" : "REPEATER", "name" : "R1"}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully added R1")

    def test11_modifying_device_strength_with_invalid_value(self):
        call = self.app.post('/ajiranet/process',
                             data='''MODIFY /devices/A1/strength
                             content-type : application/json

                             {"value": "Helloworld"}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "value should be an integer")

    def test12_modifying_device_strength_for_non_existing_device(self):
        call = self.app.post('/ajiranet/process',
                             data='''MODIFY /devices/A10/strength
                             content-type : application/json

                             {"value": "Helloworld"}''')
        self.assertEqual(call.status, "404 NOT FOUND")
        self.assertEqual(call.json["msg"], "Device not found")

    def test13_modifying_device_strength_for_existing_device(self):
        call = self.app.post('/ajiranet/process',
                             data='''MODIFY /devices/A1/strength
                             content-type : application/json

                             {"value": 2}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully defined strength")

    def test14_create_connections_for_existing_devices(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "A1", "targets" : ["A2", "A3"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")


    def test15_create_connections_to_itself(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "A1", "targets" : ["A1"]}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Cannot connect device to itself")


    def test16_create_connections_for_already_connected_devices(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                                     content-type : application/json

                                     {"source" : "A1", "targets" : ["A2"]}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Devices are already connected")

    def test17_create_connections_for_existing_devices_a5_a4(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "A5", "targets" : ["A4"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test18_create_connections_for_existing_devices_r1_a2(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "R1", "targets" : ["A2"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test19_create_connections_for_existing_devices_r1_a5(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "R1", "targets" : ["A5"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test19_create_connections_with_invalid_syntax(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "R1"}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Invalid command syntax")

    def test20_create_connections_with_invalid_syntax(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Invalid command syntax")

    def test20_create_connections_for_non_existing_node(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "A8", "targets" : ["A1"]}''')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Node 'A8' not found")

    def test21_create_connections_for_existing_devices_a2_a4(self):
        call = self.app.post('/ajiranet/process',
                             data='''CREATE /connections
                             content-type : application/json

                             {"source" : "A2", "targets" : ["A4"]}''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Successfully connected")

    def test22_get_route_for_a1_a4(self):
        call = self.app.post('/ajiranet/process',
                             data='''FETCH /info-routes?from=A1&to=A4''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Route is A1->A2->A4")

    def test23_get_route_for_a1_a5(self):
        call = self.app.post('/ajiranet/process',
                             data='''FETCH /info-routes?from=A1&to=A5''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Route is A1->A2->R1->A5")

    def test24_get_route_for_a4_a3(self):
        call = self.app.post('/ajiranet/process',
                             data='''FETCH /info-routes?from=A4&to=A3''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Route is A4->A2->A1->A3")

    def test25_get_route_for_a1_a1(self):
        call = self.app.post('/ajiranet/process',
                             data='''FETCH /info-routes?from=A1&to=A1''')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"], "Route is A1->A1")



if __name__ == '__main__':
    unittest.main()
