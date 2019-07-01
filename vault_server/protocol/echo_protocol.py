import json

class EchoProtocol:
    def process(self, message: str) -> str:
        message_obj = json.loads(message)
        modified_value = ''
        if 'value' in message_obj:
            modified_value = 'this is the result of %s' % message_obj['value'][12:]

        response_obj = dict(
            id=message_obj['id'],
            value=modified_value
        )

        return json.dumps(response_obj)