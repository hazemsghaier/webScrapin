# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field



class SsrDataCollectionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class JumiaProduct(Item):
    price=Field()
    name=Field()
    discount=Field()
    prix_precedent=Field()
    categorie=Field()
    brand=Field()
    product_page_link=Field()
    image_url=Field()
    nombre_des_article_restent=Field()
class TunisiaNetProduct(Item):
    price=Field()
    description=Field()
    lien_produit=Field()
    name=Field()
    image_url=Field()
    regular_price=Field()
    discount=Field()
    stock_availability=Field()