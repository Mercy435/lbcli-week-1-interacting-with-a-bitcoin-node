from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
def main():
    try:
        # Connect to Bitcoin Core RPC with basic credentials
        rpc_user = "alice"
        rpc_password = "password"
        rpc_host = "127.0.0.1"
        rpc_port = 18443
        base_rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

        # General client for non-wallet-specific commands
        client = AuthServiceProxy(base_rpc_url)

        # Get blockchain info
        blockchain_info = client.getblockchaininfo()

        print("Blockchain Info:", blockchain_info)

        # Create/Load the wallets, named 'Miner' and 'Trader'. Have logic to optionally create/load them if they do not exist or are not loaded already.
       #logic to optionally create/load them if they do not exist or are not loaded already.
        def get_wallet_rpc(base_url, wallet_name):
            """
            Return an AuthServiceProxy instance scoped to the given wallet.
            """
            wallet_url = f"{base_url}/wallet/{wallet_name}"
            return AuthServiceProxy(wallet_url)

        def load_or_create_wallet(client, base_url, wallet_name):                               
            """
            Load the wallet if it exists and is loaded.
            If exists but not loaded, load it.
            If does not exist, create and load it.
            Returns a wallet-specific AuthServiceProxy client.
            """
            wallets_on_disk = [w['name'] for w in client.listwalletdir()['wallets']]
            wallets_loaded = client.listwallets()

            if wallet_name not in wallets_on_disk:
                client.createwallet(wallet_name)
            elif wallet_name not in wallets_loaded:
                client.loadwallet(wallet_name)

            return get_wallet_rpc(base_url, wallet_name)



        # Create/Load the wallets, named 'Miner' and 'Trader'
        miner_wallet = load_or_create_wallet(client, base_rpc_url, "Miner")
        trader_wallet = load_or_create_wallet(client, base_rpc_url, "Trader")                   
       
        # Generate spendable balances in the Miner wallet. Determine how many blocks need to be mined.
        # block rewards only become spendable after 100 confirmations; generate an address to mine blocks to.
        blocks_to_mine = 101
        miner_address = miner_wallet.getnewaddress()
        client.generatetoaddress(blocks_to_mine, miner_address) #generates hash of blocks generated

        # Load the Trader wallet and generate a new address.
        trader_address = trader_wallet.getnewaddress()

        # Send 20 BTC from Miner to Trader.
        miner_start_balance = miner_wallet.getbalance()        
        txid = miner_wallet.sendtoaddress(trader_address, 20.0) #returns the transaction id.        
        
        # Check the transaction in the mempool.
        mempool = client.getrawmempool() #returns all transaction ids in memory pool as a json array of string transaction ids.
        if txid in mempool:
            print("Transaction is in the mempool.")
            
        # Mine 1 block to confirm the transaction.
        client.generatetoaddress(1, miner_address)
        
        # Extract all required transaction details.
        tx_details = miner_wallet.gettransaction(txid)  
              
        raw_tx = miner_wallet.getrawtransaction(txid) #generate rawtx to get miners change address and amount
        decoded_tx = miner_wallet.decoderawtransaction(raw_tx)
        
        # Write the data to ../out.txt in the specified format given in readme.md.
        out = [
                tx_details["txid"],
                miner_address,
                miner_start_balance,
                tx_details['details'][0]['address'],
                abs(tx_details['amount']),
                decoded_tx['vout'][1]['scriptPubKey']['address'],
                decoded_tx['vout'][1]['value'],
                tx_details['fee'],
                tx_details['blockheight'],
                tx_details['blockhash']
               ]     
        with open("out.txt", "w") as f:
            for item in out:
                f.write(f"{item}\n")

    except Exception as e:
        print(f"Error occurred: {e}")
        
if __name__ == "__main__":
    main()

