import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st

address = '0x8638851fca2f8997BC0Dd99133B24ba0196e5FB1'
contract_address = "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def load_tokens(file):
    with open(file) as f:
        data = json.load(f)
    tokens = data['tokens']
    token_by_symbol = build_dict(tokens, 'symbol')
    return token_by_symbol

def token_info_from_symbol(tokens, symbol):
    return tokens[symbol]

tokens = load_tokens('/Users/asiah/Documents/dev/risk-terminal/contracts/chains/ethereum/erc20_tokens_mainnet.json')
usdc_info = token_info_from_symbol(tokens, 'USDC')
print(usdc_info)

# address is the sender or receiver of the transaction
# contract address is for tokens

# async def sub():
#     c = Client(st.secrets['etherscan_apiKey'])
#     throttler = Throttler(rate_limit=5, period=1.0)
#     try:
#         print(await c.account.token_transfers(
#             address = '0x8638851fca2f8997BC0Dd99133B24ba0196e5FB1',
#             contract_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
#             start_block=0,
#             end_block=99999999
#         ))


#         # print(await c.stats.eth_price())
#         # print(await c.block.block_reward(123456))

#         # async for t in c.utils.token_transfers_generator(
#         #     address='0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
#         #     throttler=throttler
#         # ):
#         #     print(t)
#     finally:
#         await c.close()

# async def main():
#     await sub()

# asyncio.run(main())