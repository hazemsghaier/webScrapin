from itemadapter import ItemAdapter
import csv
from datetime import datetime
import re

class MyTek :
    def __init__(self,spider_name) :
        self.spider_name=spider_name
        self.file=None
        self.Mytek=None
    @classmethod
    def from_crawler(cls,crawler):
        spider_name=crawler.spider.name
        return cls(spider_name) 
    def open_spider(self,spider):
        if self.spider_name=="MyTek":
            self.file=open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\Mytek.csv","w",encoding="utf-8")
            fieldnames=["price","description","lien_produit","name","image_url","regular_price","discount","stock_availability","brand","category","offre","garantie"]
            self.Mytek=csv.DictWriter(self.file,fieldnames=fieldnames)
            self.Mytek.writeheader()
    def process_item(self,item,spider):
        if self.spider_name=="MyTek" :
            item_adapter=ItemAdapter(item)
            item_dict=dict(item)
            description=item_adapter.get("description")
            description[0]=self.description_filter(description[0])


            garantie=self.get_garantie(description[0])
            item_dict["description"]= description[0]
            item_dict["price"]=self.prices_filtring(item_adapter.get("price"))
            item_dict["discount"]=self.prices_filtring(item_adapter.get("discount"))
            item_dict["regular_price"]=self.prices_filtring(item_adapter.get("regular_price"))
            item_dict["garantie"]=garantie
            if len(description)==2:
             description[1]=self.description_filter(description[1])

             item_dict["offre"]=description[1]
            else:
                item_dict["offre"]="N/A"

            self.Mytek.writerow(item_dict)



            

            return item
        else:
            return item
    def description_filter(self,description) :
        description.replace("\xa0","")
        description.replace("\u202f","")
        description.replace("\u2003","")
        description.replace("\u2002","")
        description.replace("\u2009","")

        return description

    def get_offre(self,desc):
        pass
    def get_garantie(self,desc) :
        garantie_pattern=re.compile(r"Garantie.*(\d)+.*(ans|an|mois)",re.IGNORECASE)
        garantie=garantie_pattern.search(desc)
        if garantie != None:
            if garantie.group(2)=="mois":
                return int(garantie.group(1))
            else:
                return int(garantie.group(1))*12
    def close_spider(self,spider):
        if self.spider_name=="MyTek":
            self.file.close()
    def spider_closed(self, spider):
        if self.spider_name=="MyTek":
            finish_time = datetime.now()
            elapsed_time = finish_time - self.start_time
            spider.logger.info(f"Spider closed: {spider.name}, elapsed time: {elapsed_time}")   
    def spider_opened(self, spider):
        pass
    def prices_filtring(self,price):
            if price != "N/A":
                price=price.replace("DT","")
                price=price.replace("dt","")
                price=price.replace("\xa0","")
                price=price.replace("\u202f","")
                price=price.replace("\u2003","")
                price=price.replace("\u2002","")
                price=price.replace("\u2009","")
                price=price.replace(",",".")
                return float(price)
            else:
                return float(0)
                

