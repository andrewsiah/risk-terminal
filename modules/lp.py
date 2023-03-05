import time
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
bnb_busd_pool = protocols['bnb_busd']['address']

# address is the sender or receiver of the transaction
# contract address is for token

async def sub():
    c = Client(st.secrets['bscscan_apiKey'], api_kind='bsc')
    throttler = Throttler(rate_limit=5, period=1.0)
    try:
        transfers = await c.account.token_transfers(
            address = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
            contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            start_block=25186796,
            end_block=99999999
        )
        last_block = transfers[-1]['blockNumber']

        for i in range(1, 2):
            
            transfers.extend(await c.account.token_transfers(
                address = bnb_busd_pool,
                contract_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
                start_block=last_block,
                end_block=99999999
            ))
            last_block = transfers[-1]['blockNumber']
            print(last_block + " " + str(i))
            


        df = pd.DataFrame(transfers)
        # print(df.head())
        # with open('output/transfers.txt', 'w') as fout:
        #     json.dump(transfers, fout, ensure_ascii=False, indent=4)
        

        values_per_account = {}
        avg_trade_size = {}
        address_to_num_trades = {}

        for transfer in transfers:
            tx_from = await c.proxy.tx_by_hash(transfer['hash'])
            print("wokring")
            if transfer['from'] not in values_per_account:
                values_per_account[tx_from['from']] = int(transfer['value'])
                address_to_num_trades[tx_from['from']] = 1
                avg_trade_size[tx_from['from']] = int(transfer['value'])
            elif transfer['to'] not in values_per_account:
                values_per_account[tx_from['from']] = int(transfer['value'])
                address_to_num_trades[tx_from['from']] = 1
                avg_trade_size[tx_from['from']] = int(transfer['value'])
            else:
                values_per_account[tx_from['from']] += int(transfer['value'])
                address_to_num_trades[tx_from['from']] += 1
                avg_trade_size[tx_from['from']] += int(transfer['value'])
            time.sleep(0.15)

               
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
        
        print("done")


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

