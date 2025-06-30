# Get blockchain info using bitcoin-cli
blockchain_info=$(bitcoin-cli getblockchaininfo)

# Print the blockchain info
echo "$blockchain_info"

# Create/Load the wallets, named 'Miner' and 'Trader'. Have logic to optionally create/load them if they do not exist or not loaded already.

# wallets=("Miner" "Trader")

# for wallet in "${wallets[@]}"; do
#   # Check if wallet is loaded
#   loaded_wallets=$(bitcoin-cli -regtest listwallets)
#   if [[ "$loaded_wallets" == *"$wallet"* ]]; then
#     echo "Wallet '$wallet' is already loaded."
#   else
#     # Try to load wallet if it exists
#     if bitcoin-cli -regtest loadwallet "$wallet" 2>/dev/null; then
#       echo "Loaded existing wallet '$wallet'."
#     else
#       # If loadwallet fails, create it
#       echo "Creating wallet '$wallet'..."
#       bitcoin-cli -regtest createwallet "$wallet"
#     fi
#   fi
# done
# Generate spendable balances in the Miner wallet. How many blocks needs to be mined?

# Load Trader wallet and generate a new address

# Send 20 BTC from Miner to Trader

# Check transaction in mempool

# Mine 1 block to confirm the transaction

# Extract all required transaction details

# Write the data to ../out.txt in the specified format given in readme.md