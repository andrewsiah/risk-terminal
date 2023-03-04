import web3
import requests
import pandas as pd
import asyncio

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st

async def sub():
    c = Client(st.secrets['etherscan_apiKey'])
    throttler = Throttler(rate_limit=5, period=1.0)
    try:
        print(await c.stats.eth_price())
        print(await c.block.block_reward(123456))

        async for t in c.utils.token_transfers_generator(
            address='0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
            throttler=throttler
        ):
            print(t)
    finally:
        await c.close()

async def main():
    await sub()

asyncio.run(main())