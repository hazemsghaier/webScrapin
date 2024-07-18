import json
from itemadapter import ItemAdapter
import csv

class JumiaDataProcess:
    def __init__(self,spider_name) :
        self.spider_name=spider_name
        self.file=None
        self.log=open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\log.txt","w")
    @classmethod    
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        return cls(spider_name)
    def open_spider(self, spider):
        # Initialize an empty list to store items
        self.file=open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\jumia.csv","w",encoding="utf-8")
        fieldnames=["price","name","discount","prix_precedent","brand","categorie","product_page_link","image_url","nombre_des_article_restent","description"]
        self.jumia=csv.DictWriter(self.file,fieldnames)
        

    def process_item(self, item, spider):
        # Convert the item to a dictionary and add it to the list
        if self.spider_name=="jumia":
            item_adapter = ItemAdapter(item)
            item_dict=dict(item)
            item_dict["price"]=self.prices_filtring(item_adapter.get("price"))
            item_dict["prix_precedent"]=self.prices_filtring(item_adapter.get("prix_precedent"))
            self.jumia.writerow(item_dict)


            return item
        else :
            
            return item
    def prices_filtring(self,price):
        try :
            if price == "N/A":
                return 0
            price=price.strip()
            price=price.replace("TND","")
            price=price.replace("TND","")

            return float(price)
        except:
            self.log.write(price)

        

    def close_spider(self, spider):
        pass
