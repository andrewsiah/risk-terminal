import requests
import pandas as pd
import json


def get_security(pool_path, pool):
    def load_pools(file):
        def build_dict(seq, key):
            return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

        with open(file) as f:
            data = json.load(f)
        pools_by_name = build_dict(data['pools'], 'name')
        return pools_by_name
    pools = load_pools(pool_path)

    def get_url_addr(pools,name):
        url = pools[name]['url']
        addr = pools[name]['address']
        return url, addr

    def get_address_security(addr):
        return requests.get(f"https://api.gopluslabs.io/api/v1/address_security/{addr}?chain_id=56")

    def get_dapp_security(url):
        return requests.get(f"https://api.gopluslabs.io/api/v1/dapp_security?url={url}?chain=bsc")

    url, addr = get_url_addr(pools, pool)
    dapp_security = get_dapp_security(url)
    address_security = get_address_security(addr)
    return dapp_security.json()['result'], address_security.json()['result']
