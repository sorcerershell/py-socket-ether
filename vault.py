#!/usr/bin/env python3
import sys
import logging
import os
from dotenv import load_dotenv
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


def setup_vault(log: logging.Logger) -> VaultServer:
    PROVIDER = os.getenv('PROVIDER')
    log.info("using PROVIDER %s" % PROVIDER)
    if PROVIDER == '' or PROVIDER is None:
        raise Exception('missing PROVIDER environment')
    web3 = Web3(HTTPProvider(PROVIDER))
    sign_transfer_protocol = SignTransferProtocol(log, web3)
    echo_protocol = EchoProtocol()
    vault = VaultServer(log, echo_protocol, sign_transfer_protocol)
    return vault


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: vault [socket_path]")
        sys.exit(-1)

    SOCKET_PATH = sys.argv[1]

    load_dotenv(verbose=True)

    log = setup_logger()
    vault = setup_vault(log)

    vault.listen(SOCKET_PATH)
