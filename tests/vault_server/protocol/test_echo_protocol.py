import json
import unittest
from vault_server.protocol import EchoProtocol

class TestEchoProtocol(unittest.TestCase):
    def test_echo_response_message_should_have_same_id_with_request(self):
        request_object = dict(
            id=1
        )
        echo = EchoProtocol()
        request_msg = json.dumps(request_object)
        response_msg = echo.process(request_msg)
        response_obj = json.loads(response_msg)
        self.assertEqual(response_obj['id'], 1)

    def test_echo_response_message_should_have_same_id_with_request_and_modified_value(self):
        request_object = dict(
            id=1,
            value="this is the first command"
        )
        echo = EchoProtocol()
        request_msg = json.dumps(request_object)
        response_msg = echo.process(request_msg)
        response_obj = json.loads(response_msg)
        self.assertEqual(response_obj['id'], 1)
        self.assertEqual(response_obj['value'], 'this is the result of first command')


