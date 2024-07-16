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
            title=item_adapter.get("name")
            brand=item_adapter.get("brand")
            print(self.get_garantie(desc))
            print(self.get_offre(desc))
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
    
    def get_garantie(self,description) :
        garantie_pattern=re.compile(r"Garantie.*(\d)+.*(ans|an|mois)")
        garantie=garantie_pattern.search(description)
        if garantie :
            if garantie.group(2)=="mois":
                return int(garantie.group(1))
            else :
                return  int(garantie.group(1)*12)
        else:
            return 0
        
    def get_offre(self,desc) :
        offre_pattern = re.compile(r"Garantie.*\d.*(ans|an).*?(avec|\+).*?(.*)", re.IGNORECASE)
        match = offre_pattern.search(desc)
        if match:
          offre = match.group(3).strip()
          #to clear the description from unneeded information
          modified_text = desc[:match.start(3)] + desc[match.end(3):]
          offre=offre.split("+")
          return offre
        else:
          return "no offer"
    def add_to_csv(self,data):
        pass
