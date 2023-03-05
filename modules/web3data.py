import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st


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
pc_router = protocols['pc_router']['address']

# address is the sender or receiver of the transaction
# contract address is for token

async def sub():
    c = Client(st.secrets['bscscan_apiKey'], api_kind='bsc')
    throttler = Throttler(rate_limit=5, period=1.0)
    try:
        transfers = await c.account.token_transfers(
            address = pc_router,
            contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            start_block=25186796,
            end_block=99999999
        )
        transfers.extend(await c.account.token_transfers(
            address = pc_router,
            contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            start_block=25186796 + 10_000,
            end_block=99999999
        ))
        transfers.extend(await c.account.token_transfers(
            address = pc_router,
            contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            start_block=25186796 + 20_000,
            end_block=99999999
        ))
        transfers.extend(await c.account.token_transfers(
            address = pc_router,
            contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            start_block=25186796 + 30_000,
            end_block=99999999
        ))
        df = pd.DataFrame(transfers)
        print(df.head())
        with open('output/transfers.txt', 'w') as fout:
            json.dump(transfers, fout, ensure_ascii=False, indent=4)

        values_per_account = {}
        for transfer in transfers:
            if transfer['from'] not in values_per_account:
                values_per_account[transfer['from']] = int(transfer['value'])
            elif transfer['to'] not in values_per_account:
                values_per_account[transfer['to']] = int(transfer['value'])
            else:
                values_per_account[transfer['from']] += int(transfer['value'])
                values_per_account[transfer['to']] += int(transfer['value'])

        avg_trade_size = {}
        address_to_num_trades = {}
        for transfer in transfers:
            if transfer['from'] not in avg_trade_size:
                address_to_num_trades[transfer['from']] = 1
                avg_trade_size[transfer['from']] = int(transfer['value'])
            elif transfer['to'] not in avg_trade_size:
                address_to_num_trades[transfer['to']] = 1
                avg_trade_size[transfer['to']] = int(transfer['value'])
            else:
                address_to_num_trades[transfer['from']] += 1
                address_to_num_trades[transfer['to']] += 1
                avg_trade_size[transfer['from']] += int(transfer['value'])
                avg_trade_size[transfer['to']] += int(transfer['value'])

        for key, value in avg_trade_size.items():
            avg_trade_size[key] = (value / 10e18) / address_to_num_trades[key]
            
        for key, value in values_per_account.items():
            values_per_account[key] = value / 1e18

        sorted_avg_trade_size = pd.DataFrame(sorted(avg_trade_size.items(), key=lambda x: x[1], reverse=True))
        print(sorted_avg_trade_size.head())
        print(sorted_avg_trade_size.tail())

        
        sorted_total_size = pd.DataFrame(sorted(values_per_account.items(), key=lambda x: x[1], reverse=True))
        print(sorted_total_size.head())
        print(sorted_total_size.tail())

        sorted_num_trades = pd.DataFrame(sorted(address_to_num_trades.items(), key=lambda x: x[1], reverse=True))
        print(sorted_num_trades.head())
        print(sorted_num_trades.tail())

        with open('output/total_size.txt', 'w') as fout:
            json.dump(sorted(values_per_account.items(), key=lambda x: x[1], reverse=True), fout, ensure_ascii=False, indent=4)

        with open('output/avg_trade_size.txt', 'w') as fout:
            json.dump(sorted(avg_trade_size.items(), key=lambda x: x[1], reverse=True), fout, ensure_ascii=False, indent=4)

        with open('output/num_trades.txt', 'w') as fout:
            json.dump(sorted(address_to_num_trades.items(), key=lambda x: x[1], reverse=True), fout, ensure_ascii=False, indent=4)
        
        

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

