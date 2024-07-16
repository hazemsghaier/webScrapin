import json
from itemadapter import ItemAdapter
import logging

class JumiaDataProcess:
    def __init__(self,spider_name) :
        self.spider_name=spider_name
    @classmethod    
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        return cls(spider_name)
    def open_spider(self, spider):
        # Initialize an empty list to store items
        self.items = []

    def process_item(self, item, spider):
        # Convert the item to a dictionary and add it to the list
        if self.spider_name=="jumia":
            item_dict = ItemAdapter(item).asdict()
            self.items.append(item_dict)
            return item
        else :
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            return item

    def close_spider(self, spider):
        # Write the list of items to the JSON file when the spider closes

        try:
            if self.spider_name=="jumia":
                with open("all_data.json", "w", encoding="utf-8") as f:
                    json.dump(self.items, f, ensure_ascii=False, indent=4)
                    logging.info("Fichier all_data.json écrit et fermé avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'écriture ou de la fermeture du fichier : {e}")
            raise e
