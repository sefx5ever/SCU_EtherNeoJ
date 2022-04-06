from scuEtherNeoJ import Etherscan

eth = Etherscan(['0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb'])
resp = eth.req_etherscan()
print(resp)
print("END")