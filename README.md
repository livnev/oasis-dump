# oasis-dump

A simple tool to dump the current state of the orderbook and historical trades from an OasisDEX contract.

Source code of the OasisDEX contracts: <https://github.com/makerdao/maker-otc>.

## Installation

This project uses *Python 3.6.2*.

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/reverendus/oasis-dump.git
pip3 install -r requirements.txt
```

## Usage

```
usage: oasis-dump.py [-h] [--rpc-host RPC_HOST] [--rpc-port RPC_PORT]
                     (--orders | --trades)
                     contract

positional arguments:
  contract             Ethereum address of the OasisDEX smart contract

optional arguments:
  -h, --help           show this help message and exit
  --rpc-host RPC_HOST  JSON-RPC host (default: `localhost')
  --rpc-port RPC_PORT  JSON-RPC port (default: `8545')
  --orders             Dumps the current state of the OasisDEX orderbook
  --trades             Dumps all historical trades from the OasisDEX contract
```

## License

See [COPYING](https://github.com/reverendus/oasis-dump/blob/master/COPYING) file.
