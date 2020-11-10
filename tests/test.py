import unittest
from server import app


class NetworkSimulatorTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_calling_endpoint_with_valid_data_returns_200_response(self):
        call = self.app.post('/ajiranet/process', data = 'CREATE /devices \n content-type : application/json \n {'
                                                         '"type" : "COMPUTER", "name" : "A1"}')
        self.assertEqual(call.status, "200 OK")

    def test_calling_endpoint_with_invalid_data_returns_400_response(self):
        call = self.app.post('/ajiranet/process', data = 'CREATE /devices \n content-type : application/json')
        self.assertEqual(call.status, "400 BAD REQUEST")


if __name__ == '__main__':
    unittest.main()
