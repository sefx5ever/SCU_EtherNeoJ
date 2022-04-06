import requests, os
import pandas as pd
from lxml import etree
from time import sleep
from datetime import datetime as dt
from neo4j import GraphDatabase

class Etherscan:
    def __init__(
            self,
            addresses:list|set,
            hierarchy:int=3,
            extra_info:bool=True,
            by_hrchy:bool=True,
            by_addr:bool=False
        ):
        self.addresses = addresses
        self.hierarchy = hierarchy
        self.extra_info = extra_info
        self.by_hrchy = by_hrchy
        self.by_addr  = by_addr
        self.ether_api_base = "https://etherscan.io/"
        self.headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

    def req_etherscan(self):
        self.next_lvl_addr = []
        err_addr = []
        data_to_df = []

        try:
            for lvl in range(1,self.hierarchy+1):
                print(f"【Start Crawling Etherscan Data of Level {lvl}/{self.hierarchy}】" + "="*30)

                self.addresses = set(self.next_lvl_addr) if lvl > 1 else self.addresses
                for tar_addr in self.addresses:
                    res = self.__start_scraping_proc(tar_addr)
                    
                    if isinstance(res,list):
                        data_to_df.extend(res)
                    if isinstance(res,str):
                        err_addr.append(res)

                if self.by_hrchy:
                    self.save_as_csv(data_to_df,lvl)

                if data_to_df:
                    self.next_lvl_addr += self.__get_from_to_addr_list(data_to_df)

                data_to_df = []
                print(f"【Finished Crawling Etherscan Data of Level {lvl}/{self.hierarchy}】" + "="*27)
        except Exception as err:
            print(f"【Error/req_etherscan】Request Etherscan failed because of {err}")

        print("="*32 + f"【Summary of Etherscan Web Scrapy】" + "="*32)
        print(f"{err_addr}",end="""\n 
            These are the error address that didn't request or scrap successfully! 
            Copy the error address list and re-do in the req_etherscan function
            and set the parameter of hierarchy in 1.
        """)
        return data_to_df

    def __get_from_to_addr_list(self,data_to_df:list):
        addr_list = []

        for each in data_to_df:
            if (each['from'] is not None) and (each['from'].startswith("0x")) and (len(each['from']) == 42):
                addr_list.append(each['from'])

            if (each['to'] is not None) and (each['to'].startswith("0x")) and (len(each['to']) == 42):
                addr_list.append(each['to'])
        return addr_list

    def __req_txn_date(self,txn_hash:str):
        link = self.ether_api_base + f"tx/{txn_hash}"
        res = requests.get(link,headers=self.headers)
        # print(f"【RequestEach】: {res.status_code}")
        raw_data = etree.HTML(res.text)
        return self.__parse_date_input_data(raw_data)

    def __start_scraping_proc(self,tar_addr:str):
        stop = False
        page_num = 1
        status_bar_count = 0
        print(f'【{tar_addr}】Crawling...')

        try:
            while(not stop):
                raw_data,total_page,total_rows = self.__req_etherscan(tar_addr,page_num)
                temp_tar_row_data = []
                
                for row_no in range(1,total_rows+1):
                    temp_tar_row_data.append(self.__parse_row_data(raw_data,row_no))
                            
                status_bar_count += self.print_status_bar(page_num,total_page,status_bar_count)
                self.__sleep_by_case()
                
                if page_num >= total_page:
                    stop = True
                page_num+=1

            if self.by_addr:
                self.save_as_csv(temp_tar_row_data,f"{tar_addr[-5:]}]")
            
            return temp_tar_row_data
        except Exception as err:
            print(f"【Error/__start_scraping_proc】Failed in scrapping address {tar_addr} because of {err}")
            return tar_addr

    def print_status_bar(self,curr:int,total:int,now:int):
        try: 
            num_to_print = int((curr/total)*100) - now
        except ZeroDivisionError:
            print(f"【Error/print_status_bar】Request might be block!")
            return 0
        except Exception as err:
            print(f"【Error/print_status_bar】Error occurred in the row number {curr}/{total} because of {err}")
        
        if num_to_print+now == 100:
            print("=" * num_to_print)
        else:
            print("=" * num_to_print,end="")
        return num_to_print

    def get_curr_datatime(self):
        now = dt.now()
        return now.strftime("%Y_%m_%d_%H_%M")

    def save_as_csv(self,data_to_df:list,suffix:str|int):
        columns = data_to_df[0].keys()
        df = pd.DataFrame(data_to_df,columns=columns)
        filename = f"{self.get_curr_datatime()}_EtherNeoJ_{suffix}.scv"

        try:
            df.to_csv(filename,encoding='utf-8')
            print(f"【{filename}】Export successfully! The data's shape is {df.shape}.")
        except Exception as err:
            print(f"【Error/save_as_csv】Data export in the suffix of {filename} failed because of {err}")

    def __sleep_by_case(self,sec:int=None):
        if sec is not None:
            sleep(sec)
        elif self.extra_info:
            sleep(10)
        else:
            sleep(1)

    def __req_etherscan(self,tar_addr:str,page_num:int):
        link = self.ether_api_base + f'txs?a={tar_addr}&p={page_num}'
        res = requests.get(link,headers=self.headers)

        # print(f"【RequestAll】: {res.status_code}")

        if res.status_code == 200:
            raw_data = etree.HTML(res.text)
            return raw_data,self.__parse_total_page(raw_data),self.__parse_total_row(raw_data)
        else:
            print(f"【Error/__req_etherscan】{link} Data request failed! Restart in 3 seconds")
            self.__sleep_by_case(10)
            return self.__req_etherscan(tar_addr,page_num)

    def __parse_total_page(self,raw_data:object):
        try:
            return int(raw_data.xpath("//div[@id='ContentPlaceHolder1_topPageDiv']//strong[@class='font-weight-medium'][2]/text()")[-1])
            # return 1
        except Exception as err:
            print(f"【Error/__parse_total_page】Get total page failed because of {err}")
            return 0

    def __parse_total_row(self,raw_data:object):
        try:
            return len(raw_data.xpath("//tbody/tr"))
        except Exception as err:
            print(f"【Error/__parse_total_row】Get total row failed because of {err}")
            return 0

    def __parse_row_data(self,raw_data:object,row_no:int):
        base_path = f"//tbody/tr[{row_no}]/td"
        data = {
            'txn' : raw_data.xpath(base_path + "[2]/span/a/text()")[-1],
            'method' : raw_data.xpath(base_path + "[3]/span")[0].get('title'),
            'block' : raw_data.xpath(base_path + "[4]/a/text()")[-1],
            'age' : raw_data.xpath(base_path + "[6]/span/text()")[-1],
            'value' : raw_data.xpath(base_path + "[10]/text()")[-1],
            'txn_fee' : '.'.join(raw_data.xpath(base_path + "[11]/span/text()"))
        }

        try: ## FROM ##
            if raw_data.xpath(base_path + "[7]/span/a"):
                data['from'] = raw_data.xpath(base_path + "[7]/span/a/text()")[-1]
            elif raw_data.xpath(base_path + "[7]/a"):
                data['from'] = raw_data.xpath(base_path + "[7]/a/text()")[-1]
            elif raw_data.xpath(base_path + "[7]/span"):
                data['from'] = raw_data.xpath(base_path + "[7]/span/text()")[-1]
            else:
                data['from'] = None
        except Exception as err:
            print(f"【Error/__parse_row_data/from】\"\FROM\"\ Parsing failed because of {err}")

        try: ## TO ##
            if raw_data.xpath(base_path + "[9]/span/span"):
                data['to'] = raw_data.xpath(base_path + "[9]/span/span")[-1].attrib['title']
            elif raw_data.xpath(base_path + "[9]/span/span/a"):
                data['to'] = raw_data.xpath(base_path + "[9]/span/span/text()")[-1]
            elif raw_data.xpath(base_path + "[9]/span/a"):
                data['to'] = raw_data.xpath(base_path + "[9]/span/a/text()")[-1]
            elif raw_data.xpath(base_path + "[9]/a"):
                data['to'] = raw_data.xpath(base_path + "[9]/a/text()")[-1]
            elif raw_data.xpath(base_path + "[9]/span"):
                data['to'] = raw_data.xpath(base_path + "[9]/span/text()")[-1]
            else:
                data['to'] = None
        except Exception as err:
            print(f"【Error/__parse_row_data/to】\"\TO\"\ Parsing failed because of {err}")
        
        if self.extra_info:
            data.update(self.__req_txn_date(data['txn']))

        return data

    def __parse_date_input_data(self,raw_data:object):
        temp = dict()
        try:
            datetime_path = "//div[@id='ContentPlaceHolder1_divTimeStamp']//div[@class='col-md-9']/text()[2]"
            input_data_path = "//div[@id='ContentPlaceHolder1_collapseContent']//div[@id='rawtab']//textarea/text()"
            
            if raw_data.xpath(datetime_path):
                temp["datetime"] = raw_data.xpath(datetime_path)[-1]

            if raw_data.xpath(input_data_path):
                temp["input_data"] = raw_data.xpath(input_data_path)[-1]

            return temp
        except Exception as err:
            print(f"【Error/__parse_date_input_data】Date and Input Data parsing failed because of {err}")