from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
rpc_user = "alice"
rpc_password = "password"
rpc_host = "127.0.0.1"
rpc_port = 18443
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
# rpc_connection = AuthServiceProxy(
#     "http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port),
#     timeout=120)
best_block_hash = rpc_connection.getbestblockhash()
print(rpc_connection.getblock(best_block_hash))


