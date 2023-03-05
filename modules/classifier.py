import web3
import requests
import pandas as pd
import asyncio
import json

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st

trade_sizes = pd.read_json("output/total_size.txt")
num_of_trades = pd.read_json("output/num_trades.txt")
avg_trade_size = pd.read_json("output/avg_trade_size.txt")
# net_worth = pd.read_json("output/balances.txt")

classifications = {}
for i in trade_sizes[0]:
    classifications[i] = []

print(classifications)