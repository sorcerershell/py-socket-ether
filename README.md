# VAULT
Vault is a small server that listen to specified unix socket. This server will handle 2 kind of requests:
1. Echo Request
Message send to this server will replied back with the same message but with modified value. 
2. Sign Transfer Request (Ether)
Message send to this server will sign ethereum transaction 
that later can be broadcasted to ethereum network 


## Requirements
- Python 3
- web3
- python-dotenv

## How to install
```bash
$ cp env.example .env
$ pip3 install -r requirements.txt
```

## How to run
- Run the Server
```bash
$ python3 vault.py vault.sock
```
- Run the client
```bash
$ python3 vault_client.py vault.sock
```

## How to configure
### Change ethereum network
You can change ethereum network inside .env file. 
Currently limited to ropsten network.

### Change sender account
1. Inside vault_client.py, change FROM_ADDRESS constant on top of the file.
2. Put your private key inside folder .keys with this format: [account_hex].key

### Change receiving account
1. Inside vault_client.py, change TO_ADDRESS constant on top of the file.


