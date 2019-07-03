import json
import logging
import sys
from web3 import Web3, middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy
from web3.gas_strategies.time_based import fast_gas_price_strategy
from typing import Dict


class SignTransferProtocol:
    w3: Web3
    log: logging.Logger
    request: Dict[str, str]

    def __init__(self, log: logging.Logger, w3: Web3):
        self.w3 = w3
        self.log = log

    def process(self, message: str) -> str:
        message_obj = json.loads(message)
        self.request = message_obj

        message_id = self.request['id']
        src_account = self.request['from_address']
        dst_account = self.request['to_address']
        value = Web3.toWei(self.request['amount'], 'ether')

        response = dict()
        nonce = self.fetch_nonce(src_account)
        gas = self.estimate_gas(src_account, dst_account)
        gas_price = self.estimate_gas_price()

        real_value = value - (gas * gas_price)

        try:
            self.log.debug("Opening Private Key")
            with open('./.keys/' + src_account[2:] + '.key') as keyfile:
                encrypted_key = keyfile.read()
                private_key = self.w3.eth.account.decrypt(encrypted_key, 'pocky chocolate flavour')

            txn = dict(
                nonce=nonce,
                gasPrice=gas_price,
                gas=gas,
                to=dst_account,
                value=real_value,
                chainId=3,
            )
            self.log.debug("transactions %s" % txn)
            self.log.debug('Signing Transaction')
            signed_txn = self.w3.eth.account.signTransaction(txn, private_key)
            print(signed_txn)
            response = dict(
                id=message_id,
                tx=signed_txn.rawTransaction.hex()
            )
        except IOError:
            self.log.error(IOError)

        return json.dumps(response)

    def estimate_gas(self, src_account, dst_account):
        return self.w3.eth.estimateGas({'to': self.w3.toChecksumAddress(dst_account),
                                        'from': self.w3.toChecksumAddress(src_account)})

    def fetch_nonce(self, src_account):
        return self.w3.eth.getTransactionCount(self.w3.toChecksumAddress(src_account), 'pending')

    def estimate_gas_price(self):
        self.w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
        self.w3.middleware_stack.add(middleware.time_based_cache_middleware)
        self.w3.middleware_stack.add(middleware.latest_block_based_cache_middleware)
        self.w3.middleware_stack.add(middleware.simple_cache_middleware)
        gas_price = self.w3.eth.generateGasPrice()
        return gas_price

    def value_based_gas_price_strategy(self, transaction_params):
        if transaction_params['value'] > self.w3.toWei(1, 'ether'):
            return self.w3.toWei(20, 'gwei')
        else:
            return self.w3.toWei(5, 'gwei')