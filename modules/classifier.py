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
net_worth = pd.read_json("output/balances.txt")
is_lp = pd.read_json("output/addresses.txt")
is_trader = pd.read_json("output/addresses2.txt")
net_worth2 = pd.read_json("output/balances2.txt")
avg_trade_size = pd.read_json("output/avg_trade_size.txt")

classifications = { "labels": {} }
for i in trade_sizes[0]:
    classifications["labels"][i] = []
for i in num_of_trades[0]:
    classifications["labels"][i] = []
for i in net_worth[0]:
    classifications["labels"][i] = []
for i in is_lp[0]:
    classifications["labels"][i] = []
for i in is_trader[0]:
    classifications["labels"][i] = []
for i in net_worth2[0]:
    classifications["labels"][i] = []
for i in avg_trade_size[0]:
    classifications["labels"][i] = []


for i in is_lp[0]:
    classifications["labels"][i].append("LP")

for i in is_trader[0]:
    classifications["labels"][i].append("Trader")
    #classifications["labels"][i].append("Retail")

for i in range(len(net_worth[0])):
    if int(net_worth[1][i]) > 100_000:
        classifications["labels"][net_worth[0][i]].append("Whale")
        classifications["labels"][net_worth[0][i]].append("Trader")
    elif int(net_worth[1][i]) > 60_000:
        classifications["labels"][net_worth[0][i]].append("Small Whale")
        classifications["labels"][net_worth[0][i]].append("Trader")

for i in range(len(net_worth2[0])):
    if int(net_worth2[1][i]) > 100_000:
        classifications["labels"][net_worth2[0][i]].append("Whale")
        classifications["labels"][net_worth[0][i]].append("Trader")
    elif int(net_worth2[1][i]) > 60_000:
        classifications["labels"][net_worth2[0][i]].append("Small Whale")
        classifications["labels"][net_worth[0][i]].append("Trader")

for i in range(len(trade_sizes[0])):
    if int(trade_sizes[1][i]) > 50: #if large and frequent trader, then most likely an arb
        classifications["labels"][trade_sizes[0][i]].append("Abritrageur")
    elif int(trade_sizes[1][i]) > 10:
        classifications["labels"][trade_sizes[0][i]].append("Day Trader")
for i in range(len(num_of_trades[0])):
    if int(num_of_trades[1][i]) > 3:
        classifications["labels"][num_of_trades[0][i]].append("Day Trader")
    elif int(num_of_trades[1][i]) > 1:
        classifications["labels"][num_of_trades[0][i]].append("HODLer")
for i in range(len(num_of_trades[0])):
    if int(num_of_trades[1][i]) > 40:
        classifications["labels"][num_of_trades[0][i]].append("Abritrageur")
    if int(num_of_trades[1][i]) > 10:
        classifications["labels"][num_of_trades[0][i]].append("Day Trader")
    elif int(num_of_trades[1][i]) > 1:
        classifications["labels"][num_of_trades[0][i]].append("HODLer")


# print(classifications["labels"])

with open('output/classifications.txt', 'w') as fout:
    json.dump(classifications, fout, ensure_ascii=False, indent=4)