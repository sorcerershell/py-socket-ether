#!/usr/bin/env python3
import sys
import logging
from web3 import Web3, HTTPProvider
from vault_server import VaultServer
from vault_server.protocol import EchoProtocol, SignTransferProtocol


def setup_logger() -> logging.Logger:
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    return log


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vault [socket_path]")
        sys.exit(-1)

    SOCKET_PATH = sys.argv[1]
    log = setup_logger()

    log.info('Listening to %s' % SOCKET_PATH)

    web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/8a344b20d56d406eaf81ee274bcf2a61"))
    signTransferProtocol = SignTransferProtocol(log, web3)
    echoProtocol = EchoProtocol()
    vault = VaultServer(log, echoProtocol, signTransferProtocol)
    vault.listen(SOCKET_PATH)
