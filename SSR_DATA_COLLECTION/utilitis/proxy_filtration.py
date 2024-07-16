import requests
import threading
import queue

#q = queue.Queue()
#valid_proxy_list = []

# Read proxies from file into queue
#with open(r"C:/Users/PCS/Desktop/data_collection/data-collection/SSR_DATA_COLLECTION/SSR_DATA_COLLECTION\static/valid_proxy.txt", "r") as f:
#    proxies = f.read().split("\n")
#    for proxy in proxies:
# #       q.put(proxy.strip())  # strip() to remove any leading/trailing whitespace

def check_validity():
    global q, valid_proxy_list
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("https://books.toscrape.com/", proxies={"http": proxy, "https": proxy}, timeout=5)
            if res.status_code == 200:
                valid_proxy_list.append(proxy)
        except Exception as e:
            print(f"Error with proxy {proxy}: {e}")
            continue

def create_valid_proxy_file():
    global valid_proxy_list
    with open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\valid_proxy1.txt", "w") as f:
        for proxy in valid_proxy_list:
            f.write(proxy + "\n")

# Use threading to check validity concurrently
#threads = []
#for _ in range(10):  # Adjust number of threads as needed#
   # t = threading.Thread(target=check_validity)
    ##t.start()
    #threads.append(t)

#for t in threads:#
    # t.join()

#create_valid_proxy_file()

def get_non_valide_proxy():
        res=requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc")
        json_res=res.json()
        data=json_res["data"]
        print(type(data)) 
get_non_valide_proxy()