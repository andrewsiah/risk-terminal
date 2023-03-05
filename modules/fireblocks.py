from fireblocks_sdk import FireblocksSDK, VAULT_ACCOUNT, PagedVaultAccountsRequestFilters, TransferPeerPath, DestinationTransferPeerPath
import json
import streamlit as st

def fireblocks_initiate_transactions(contract_address, fireblocks_account_id, amount):
    api_secret = open('.streamlit/home.key', 'r').read()
    api_key = st.secrets['fireblocks_apiKey']
    api_url = 'https://sandbox-api.fireblocks.io'
    fireblocks = FireblocksSDK(api_secret, api_key, api_base_url=api_url)
    initiate_transactions = fireblocks.create_transaction( asset_id="BNB", amount="5", source=TransferPeerPath(VAULT_ACCOUNT, 2), destination=DestinationTransferPeerPath(VAULT_ACCOUNT, 1) )
    print(initiate_transactions)