import socket
import json
import logging
import signal
import os
import sys
from typing import List
from vault_server.protocol import EchoProtocol, SignTransferProtocol


class VaultServer:
    log: logging.Logger
    sock: socket.socket
    socketPath: str
    echoProtocol: EchoProtocol
    kill_now = False



    def __init__(self, log: logging.Logger, echo: EchoProtocol, signTransfer: SignTransferProtocol):
        self.log = log
        self.echoProtocol = echo
        self.signTransferProtocol = signTransfer
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)



    def setup(self, socket_path: str) -> None:
        self.socketPath = socket_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.socketPath)
        self.sock.listen(1)

    def exit_gracefully(self, signum, frame):
        self.log.warning('Exiting and cleaning up...')
        self.kill_now = True
        os.remove(self.socketPath)
        sys.exit(0)


    def receive(self) -> None:
        conn, addr = self.sock.accept()
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                responses = self.process_message(data.decode("utf-8"))
                conn.sendall(responses)

    def listen(self, socket_path: str):
        self.setup(socket_path)
        while not self.kill_now:
            self.log.info('Accepting connection...')
            self.receive()

    def process_message(self, message: str) -> bytes:
        lines = message.split("\n")
        responses: List[str]
        responses = []

        for line in lines:
            self.log.debug("Received: %s" % line)

            if line == '':
                continue

            message_object = json.loads(line)

            if "value" in message_object:
                self.log.debug("message type: ECHO")
                echo_response = self.echoProtocol.process(line)
                responses.append(echo_response)

            if "type" in message_object and message_object['type'] == 'sign_transfer':
                self.log.debug("message type: SIGN TRANSFER")
                sign_response = self.signTransferProtocol.process(line)
                print(sign_response)
                responses.append(sign_response)

        response = "\n".join(responses).encode('ascii')
        return response
