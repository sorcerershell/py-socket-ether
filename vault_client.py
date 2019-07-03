#!/usr/bin/env python3
import socket
import sys
import json

FROM_ADDRESS = "0xc3a0775c1293be7abfa0a3b11f6158a8a1d720a0"
TO_ADDRESS = "0xBb3042F6a37d73AB73Bd537bC3d8E204E37Eb062"


def test_simple_echo_message():
    request_message = b"""{"id":"1", "value":"this is the first command"}"""

    print('Sending', request_message)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(request_message)
        data = s.recv(1024)

    print('Received', repr(data))

    request_message = b"""{"id":"1", "value":"this is the second command"}"""

    print('Sending', request_message)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(request_message)
        data = s.recv(1024)

    print('Received', repr(data))


def test_sign_transfer_message():
    request = dict(
        id="1",
        type="sign_transfer",
        from_address=FROM_ADDRESS,
        to_address=TO_ADDRESS,
        amount="1"
    )
    request_message = json.dumps(request).encode("ascii")

    print('Sending', request_message)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(request_message)
        data = s.recv(1024)

    print('Received', repr(data))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vault [socket_path]")
        exit(-1)

    SOCKET_PATH = sys.argv[1]

    test_simple_echo_message()
    test_sign_transfer_message()
