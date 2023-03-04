import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def load_tokens(file):
    with open(file) as f:
        data = json.load(f)
    tokens = data['tokens']
    token_by_symbol = build_dict(tokens, 'symbol')
    return token_by_symbol

tokens = load_tokens('contracts/chains/ethereum/erc20_tokens_mainnet.json')

usdc_addr = tokens['USDC']['address']
weth_addr = tokens['WETH']['address']
wbtc_addr = tokens['WBTC']['address']
dai_addr  = tokens['DAI']['address']
usdt_addr = tokens['USDT']['address']
uni_addr  = tokens['UNI']['address']
link_addr = tokens['LINK']['address']

def load_wallets(file):
    with open(file) as f:
        data = json.load(f)
    wallets = data['wallets']
    wallet_by_name = build_dict(wallets, 'name')
    return wallet_by_name

wallets = load_wallets('data/quants.json')

jumptrading_addr = wallets['jumptrading']['address']
# print(jumptrading_addr)

def load_protocols(file):
    with open(file) as f:
        data = json.load(f)
    protocols = data['protocols']
    protocol_by_name = build_dict(protocols, 'name')
    return protocol_by_name
protocols = load_protocols('data/protocols.json')
uniswap_v3_usdc_weth_0_5_addr = protocols['uniswap_v3_usdc_weth_0_5']['address']

# address is the sender or receiver of the transaction
# contract address is for token

async def sub():
    c = Client(st.secrets['etherscan_apiKey'])
    throttler = Throttler(rate_limit=5, period=1.0)
    try:
        transfers = await c.account.token_transfers(
            address = uniswap_v3_usdc_weth_0_5_addr,
            contract_address = weth_addr,
            start_block=16754000,
            end_block=99999999
        )
        df = pd.DataFrame(transfers)
        print(df.info())
        # with open('output/transfers.txt', 'w') as fout:
        #     json.dump(transfers, fout, ensure_ascii=False, indent=4)


        # print(await c.stats.eth_price())
        # print(await c.block.block_reward(123456))

        # async for t in c.utils.token_transfers_generator(
        #     address='0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
        #     throttler=throttler
        # ):
        #     print(t)
    finally:
        await c.close()

async def main():
    await sub()

asyncio.run(main())

