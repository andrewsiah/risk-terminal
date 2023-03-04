import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
components.iframe(
    "https://pancakeswap.finance/add/BNB/0x55d398326f99059ff775485246999027b3197955",
     height=600)

# goplusapi
contract_security = requests.get("")

0x16b9a82891338f9bA80E2D6970FddA79D1eb0daE