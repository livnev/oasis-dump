#!/usr/bin/env python3
#
# Copyright (C) 2017 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import json
from typing import Optional, List

import pkg_resources
from web3 import Web3, HTTPProvider


class OfferInfo:
    def __init__(self, offer_id: int, sell_how_much: int, sell_which_token: str, buy_how_much: int,
                 buy_which_token: str, owner: str, timestamp: int):
        self.offer_id = offer_id
        self.sell_how_much = sell_how_much
        self.sell_which_token = sell_which_token
        self.buy_how_much = buy_how_much
        self.buy_which_token = buy_which_token
        self.owner = owner
        self.timestamp = timestamp

    @staticmethod
    def _format_amount(value: int):
        tmp = str(value).zfill(19)
        return (tmp[0:len(tmp)-18] + "." + tmp[len(tmp)-18:len(tmp)]).replace("-.", "-0.")

    def __str__(self):
        return f"Offer #{self.offer_id}: {self._format_amount(self.sell_how_much)} [{self.sell_which_token}]" \
               f" for {self._format_amount(self.buy_how_much)} [{self.buy_which_token}] (owner: {self.owner})"


parser = argparse.ArgumentParser(prog='oasis-dump')
parser.add_argument("--rpc-host", help="JSON-RPC host (default: `localhost')", default="localhost", type=str)
parser.add_argument("--rpc-port", help="JSON-RPC port (default: `8545')", default=8545, type=int)
parser.add_argument("contract", help="Ethereum address of the OasisDEX smart contract", type=str)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--orders',action='store_true',help='Dumps the current state of the OasisDEX orderbook')
group.add_argument('--trades',action='store_true',help='Dumps all historical trades from the OasisDEC contract')

arguments = parser.parse_args()

web3 = Web3(HTTPProvider(endpoint_uri=f"http://{arguments.rpc_host}:{arguments.rpc_port}"))
abi = json.loads(pkg_resources.resource_string(__name__, 'SimpleMarket.abi'))
contract = web3.eth.contract(abi=abi)(address=arguments.contract)

def get_offer(offer_id: int) -> Optional[OfferInfo]:
    array = contract.call().offers(offer_id)
    if array[5] is not True:
        return None
    else:
        return OfferInfo(offer_id=offer_id,
                         sell_how_much=array[0],
                         sell_which_token=array[1],
                         buy_how_much=array[2],
                         buy_which_token=array[3],
                         owner=array[4],
                         timestamp=array[6])


def print_orders():
    offers = [get_offer(offer_id + 1) for offer_id in range(contract.call().last_offer_id())]
    for offer in [offer for offer in offers if offer is not None]:
        print(offer)


if arguments.orders:
    print_orders()

# if arguments.trades:
#     print_trades()

