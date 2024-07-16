from random import randint
import requests
from SSR_DATA_COLLECTION.utilitis import constents
from concurrent.futures import ThreadPoolExecutor, as_completed

class Proxy:
    def get_non_valide_proxy_from_geonode(self, file_path_to_store=constents.non_valid_file_path):
        res = requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc")
        json_res = res.json()
        data = json_res["data"]
        with open(constents.non_valid_file_path, "w") as f:
            ch = ""
            for i in data:
                ch += i["ip"] + ":" + i["port"] + "\n"
            f.write(ch)

    def get_random_proxy(self):
        try:
            with open("valid_proxy.txt") as f:
                valid_list_of_proxys = f.read().split("\n")
                return valid_list_of_proxys[randint(0, len(valid_list_of_proxys) - 1)]
        except:
            print("something went wrong")

    def check_proxy(self, proxy):
        try:
            res = requests.get("https://books.toscrape.com/", proxies={"http": proxy, "https": proxy}, timeout=10)
            if res.status_code == 200:
                return proxy
        except Exception as e:
            print(f"Error with proxy {proxy}: {e}")
        return None

    def check_validity(self, file_path_to_read=constents.non_valid_file_path, valid_file_path=constents.valid_proxy_path):
        try:
            with open(file_path_to_read, "r") as f:
                list_of_proxys = f.read().split("\n")
                
            valid_proxy_list = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_proxy = {executor.submit(self.check_proxy, proxy): proxy for proxy in list_of_proxys}
                for future in as_completed(future_to_proxy):
                    proxy = future_to_proxy[future]
                    try:
                        result = future.result()
                        if result:
                            valid_proxy_list.append(result)
                    except Exception as e:
                        print(f"Error processing proxy {proxy}: {e}")
            
            with open(valid_file_path, "w") as f:
                for proxy in valid_proxy_list:
                    f.write(proxy + "\n")
        except Exception as e:
            print(f"An error occurred: {e}")
