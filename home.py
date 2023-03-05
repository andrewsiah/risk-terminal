import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st
import streamlit.components.v1 as components
import fireblocks_sdk

import modules.goplus as goplus

# embed streamlit docs in a streamlit app
# components.iframe(
#     "https://pancakeswap.finance/add/BNB/0x55d398326f99059ff775485246999027b3197955",
#      height=600)

dapp_security, address_security = goplus.get_security('contracts/chains/binance-smart-chain/bep20_pools.json', 'add_bnb_usdt')
st.json(dapp_security)
st.json(address_security)


