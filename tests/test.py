import unittest
from server import app


class NetworkSimulationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test1_fetching_devices_with_no_device_created_returns_empty_list(self):
        call = self.app.post('/ajiranet/process',
                             data='FETCH /devices')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["devices"], [])

    # Create devices tests
    def test2_calling_endpoint_with_valid_data_returns_200_response(self):
        call = self.app.post('/ajiranet/process', data='CREATE /devices\ncontent-type : application/json\n{'
                                                       '"type" : "COMPUTER", "name" : "C1"}')
        self.assertEqual(call.status, "200 OK")

    def test3_calling_endpoint_with_invalid_data_returns_400_response(self):
        call = self.app.post('/ajiranet/process', data='CREATE /devices \n content-type : application/json')
        self.assertEqual(call.status, "400 BAD REQUEST")

    def test4_calling_create_devices_with_valid_data_gives_success_message(self):
        call = self.app.post('/ajiranet/process',
                             data='CREATE /devices\ncontent-type : application/json\n{"type" : "COMPUTER", "name" : "B1"}')
        self.assertEqual(call.json["msg"], "Successfully added B1")

    def test5_calling_create_devices_with_existing_gives_error_message_and_400_response(self):
        call_1 = self.app.post('/ajiranet/process',
                               data='CREATE /devices\ncontent-type : application/json\n{"type" : "COMPUTER", "name" : "A1"}')
        self.assertEqual(call_1.status, "200 OK")
        call_2 = self.app.post('/ajiranet/process',
                               data='CREATE /devices\ncontent-type : application/json\n{"type" : "COMPUTER", "name" : "A1"}')
        self.assertEqual(call_2.status, "400 BAD REQUEST")
        self.assertEqual(call_2.json["msg"], "Device 'A1' already exists")

    def test6_calling_create_devices_with_invalid_type_gives_error_message_and_400_response(self):
        call = self.app.post('/ajiranet/process',
                             data='CREATE /devices\ncontent-type : application/json\n{"type" : "PHONE", "name" : "P1"}')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "type 'PHONE' is not supported")

    def test7_fetching_devices_with_devices_created_returns_device_list(self):
        call = self.app.post('/ajiranet/process',
                             data='FETCH /devices')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["devices"], [{'name': 'C1', 'type': 'COMPUTER'}, {'name': 'B1', 'type': 'COMPUTER'}, {'name': 'A1', 'type': 'COMPUTER'}])

    def test8_creating_connection_between_existing_nodes_is_successful(self):
        call = self.app.post('ajiranet/process',
                             data='CREATE /connections\ncontent-type : application/json\n{"source" : "B1", "targets" : ["A1","C1"]}')
        self.assertEqual(call.status, "200 OK")
        self.assertEqual(call.json["msg"],"Successfully connected")

    def test9_creating_connection_if_any_node_is_not_created_returns_error(self):
        call = self.app.post('ajiranet/process',
                             data='CREATE /connections\ncontent-type : application/json\n{"source" : "A8", "targets" : ["A1","C1"]}')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Node 'A8' not found")

    def test10_creating_connection_if_taget_node_is_missing_returns_invalid_syntax_error(self):
        call = self.app.post('ajiranet/process',
                             data='CREATE /connections\ncontent-type : application/json\n{"source" : "A1"')
        self.assertEqual(call.status, "400 BAD REQUEST")
        self.assertEqual(call.json["msg"], "Invalid command syntax")


if __name__ == '__main__':
    unittest.main()
