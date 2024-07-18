from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import csv

class TunisiaNet_pipeline :
    def __init__(self,spider_name) :
        self.spider_name=spider_name
        self.tunisiaNet=None
        self.file=None
    @classmethod
    def from_crawler(cls,crawler):
        spider_name=crawler.spider.name
        return cls(spider_name)
    def open_spider(self,spider):
        if "tunisiaNet"==self.spider_name:
            self.file=open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\tunisiaNet.csv","w", encoding='utf-8')
            fieldnames=["price","description","lien_produit","name","image_url","regular_price","discount","stock_availability","brand","category","offre","garantie"]
            self.tunisiaNet=csv.DictWriter(self.file,fieldnames=fieldnames)
            self.tunisiaNet.writeheader()      
      
    def process_item(self,item,spider):
        if self.spider_name=="tunisiaNet" and item != None :
            item_adapter=ItemAdapter(item)
            description=item_adapter.get("description")
            desc=self.description_filter(description)
            desc=desc.strip()
            item_dict = dict(item)
            item_dict["price"]=float(item_dict["price"].replace("\xa0","").replace("DT","").strip().replace(",","."))
            if item_dict["regular_price"] != "N/A":
                item_dict["regular_price"]=float(item_dict["regular_price"].replace("\xa0","").replace("DT","").strip().replace(",","."))
            else:
                item_dict["regular_price"]=-1.0

            if item_dict["discount"] != "N/A":
                item_dict["discount"]=float(item_dict["discount"].replace("\xa0","").replace("DT","").strip().replace(",","."))
            else:
                item_dict["discount"]=0    
            garantie=self.get_garantie(desc)
            offre=self.get_offre(desc)
            desc=desc.replace(offre,"")
            item_dict["description"]=desc
            item_dict["garantie"]=garantie
            item_dict["offre"]=offre
            item_dict["description"]=item_dict["description"].replace("\xa0","")
            self.tunisiaNet.writerow(item_dict)
            return item
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
            ch.replace("‎","")
        return ch    
    #extraction de garantie de le produit a partir du description
    def get_garantie(self,description) :
        garantie_pattern=re.compile(r"Garantie.*(\d)+.*(ans|an|mois)")
        garantie=garantie_pattern.search(description)
        if garantie :
            if garantie.group(2)=="mois":
                return int(garantie.group(1))
            else :
                return  int(garantie.group(1))*12
        else:
            return 0
    #extraction des offre du plus de le produit a partir du description
    def get_offre(self,desc) :
        offre_pattern = re.compile(r"Garantie.*\d.*(ans|an).*?(avec|\+).*?(.*)", re.IGNORECASE)
        match = offre_pattern.search(desc)
        if match:
          offre = match.group(3).strip()
          return offre
        else:
          return "no offer"
    def close_spider(self,spider) :
                if "tunisiaNet"==self.spider_name:
                     self.file.close()
