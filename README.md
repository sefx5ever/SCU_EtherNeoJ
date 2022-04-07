# scuEtherNeoJ Documentation

### Package overview
The scuEtherNeoJ is a Python package providing Etherscan web scraping function which can directly export data as csv or put the data in a graph database(Neo4j). It's easy to get started by giving an address and the optional arguments, then you will completely craw the transaction data in a hierarchy-based.

### Getting started
* How do I install the package?
Run the following command to install:
```
$ pip install scuEtherNeoJ
```

* How to import the package?
Run the following command to install:
```Python
from scuEtherNeoJ.Etherscan import Etherscan
```

### The solutions of scuEtherNeoJ package
* Solution 1: Import the unique address as a address input.
```Python
list_ = Etherscan.from_csv_to_uniq_addr("2022_03_21_Etherscan_Data_93BBB","D:/Jupyter Files/")
eth = Etherscan(list_,1,extra_info=False)
resp = eth.req_etherscan()
print(resp)
```

* Solution 2: Giving a list or set of address.
```Python
eth = Etherscan(['0xed5af388653567af2f388e6224dc7c4b3241c544'],1,extra_info=False)
resp = eth.req_etherscan()
print(resp)
```

### The perameters of package
* Etherscan
    * Description:
        Initialize the package funtion.
    * Parameters:
        * addressess :: list | set :: Required. The wallet or contract address to start scraping.
        * hierarchy :: int :: Default is 3. The level data to scrap.
        * extra_info :: bool :: Default is True. To get the input data and date info for the current scraping.
        * by_hrchy :: bool :: Default is False. To export data by hierarchy.
        * by_addr :: bool :: Default is True. To export data by address.
    * Returns:
        Object.
    * Usage:
        ```Python
        eth = Etherscan(['ADDRESSESS_TO_SCRAP'])
        ```

* req_etherscan
    * Description:
        Start to web scraping process.
    * Returns:
        List. The fail addressess in scraping.
    * Usage:
        ```Python
        resp = eth.req_etherscan()
        ```