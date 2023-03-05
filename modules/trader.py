import time
import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st

addresses = pd.read_json("output/total_size.txt")[0]

async def sub(): 
    api_key = st.secrets['covalent_apiKey']
    account_to_value = {}
    
    is_lp = {}
    url = "https://api.covalenthq.com/v1/bsc-mainnet/address/{}/transactions_v2/?key={}".format("0x10ED43C718714eb63d5aA57B78B54704E256024E", "ckey_53e97fcfb006430da191bfa3400")
    print(url)

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",            
    }

    response = requests.get(url, headers=headers)
    response = response.json()['data']['items']
    # print(response[0])
    addresses = []
    for i in range(len(response)):
        if response[i]['from_address'] not in addresses:
            addresses.append(response[i]['from_address'])

    with open('output/addresses2.txt', 'w') as fout:
        json.dump(addresses, fout, ensure_ascii=False, indent=4)
    
    
    for address in addresses:
        try:
            url = "https://api.covalenthq.com/v1/bsc-mainnet/address/{}/balances_v2/?key={}".format(address, "ckey_53e97fcfb006430da191bfa3400")
            print(url)
        
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",            
            }        

            response = requests.get(url, headers=headers)
            total = response.json()['data']['items'][0]['quote']
            for i in range(1, len(response.json()['data']['items'])):
                total += response.json()['data']['items'][i]['quote']
            account_to_value[address] = total
            # print(response)
        except:
            pass
        time.sleep(0.15)
    with open('output/balances2.txt', 'w') as fout:
        json.dump(sorted(account_to_value.items(), key=lambda x: x[1], reverse=True), fout, ensure_ascii=False, indent=4)

    # with open('output/balances.txt', 'w') as fout:
    #         json.dump(sorted(balances.items(), key=lambda x: x[1], reverse=True), fout, ensure_ascii=False, indent=4)


async def main():
    await sub()

asyncio.run(main())