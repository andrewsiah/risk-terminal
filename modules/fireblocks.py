from fireblocks_sdk import FireblocksSDK, VAULT_ACCOUNT, PagedVaultAccountsRequestFilters, TransferPeerPath, DestinationTransferPeerPath
import json
import streamlit as st

api_secret = open('.streamlit/home.key', 'r').read()
api_key = st.secrets['fireblocks_apiKey']
api_url = 'https://sandbox-api.fireblocks.io' # Choose the right api url for your workspace type 
fireblocks = FireblocksSDK(api_secret, api_key, api_base_url=api_url)


# Print vaults before creation
vault_accounts = fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters())
print(json.dumps(vault_accounts, indent = 1))

# Create new vault
vault_account = fireblocks.create_vault_account(name = "BscVault")

# Print vaults after creation
vault_accounts = fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters())
print(json.dumps(vault_accounts, indent = 1))

# initiate_transactions = fireblocks.create_transaction( asset_id="BTC", amount="50", source=TransferPeerPath(VAULT_ACCOUNT, "BscVault"), destination=DestinationTransferPeerPath(VAULT_ACCOUNT, "Quickstart_Vault") )
initiate_transactions = fireblocks.create_transaction( asset_id="BNB", amount="50", source=TransferPeerPath(VAULT_ACCOUNT, 2), destination=DestinationTransferPeerPath(VAULT_ACCOUNT, 1) )

print(initiate_transactions)