from scuEtherNeoJ.Etherscan import Etherscan

# Solution 1
list_ = Etherscan.from_csv_to_uniq_addr("2022_03_21_Etherscan_Data_93BBB","D:/Jupyter Files/")
eth = Etherscan(list_,1,extra_info=False)
resp = eth.req_etherscan()
print(resp)
print("END")

# Solution 2
eth = Etherscan(['0xed5af388653567af2f388e6224dc7c4b3241c544'],1,extra_info=False)
resp = eth.req_etherscan()
print(resp)
print("END")