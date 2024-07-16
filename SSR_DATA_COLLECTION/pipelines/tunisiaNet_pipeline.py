from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re

class TunisiaNet_pipeline :
    def __init__(self,spider_name) :
        self.spider_name=spider_name
    @classmethod
    def from_crawler(cls,crawler):
        spider_name=crawler.spider.name
        return cls(spider_name)
    def open_spider(self,spider):
        pass
    def process_item(self,item,spider):
        if self.spider_name=="tunisiaNet" and item != None :
            #filtrage et concatination du description
            item_adapter=ItemAdapter(item)
            description=item_adapter.get("description")
            desc=self.description_filter(description)
            print(self.get_garantie(desc))
            #extraction du brand
            #extraction du model
            #extraction du garantie
            #extraction du offre du plus
        else :
            return item
    def description_filter(self,description):
        ch=""
        for desc in description :
            if bool(re.fullmatch(r"\s*",desc)):
                continue
            else:
                ch=ch+desc
                continue
        return ch    

                


        
        
    def get_brand(self,data) :
        pass
    def get_garantie(self,description) :
        garantie_pattern=re.compile(r"Garantie.*\d.*(ans|an)")
        garantie=garantie_pattern.search(description)
        if garantie :
            return garantie.group()
        else:
            return "sans garantie"
        
    def get_offre(self,data) :
        pass
    def add_to_csv(self,data):
        pass