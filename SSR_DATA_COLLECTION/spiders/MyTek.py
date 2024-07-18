import scrapy
from SSR_DATA_COLLECTION.items import MyTek
import time

class MytekSpider(scrapy.Spider):
    name = "MyTek"
    allowed_domains = ["www.mytek.tn"]
    start_urls = ["https://www.mytek.tn/"]
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 15,  # Timeout en secondes
    }

    def parse(self, response):
        links=response.xpath("//li/a[@class='clearfix']/@href").getall()
       
        for link in links:
            yield response.follow(link,self.parse_product)
            
    def parse_product(self,response) :
        articals=response.css("div.column.main")
        articals=articals.css("li.product-item")
        for article in articals:
            product=MyTek()
            product["description"] = article.xpath("normalize-space(.//div/div[@class='prdtBILDetails']/div[contains(@class, 'details product-item-details')]/div[contains(@class, 'product description product-item-description')]/div/p)").getall()
            product["brand"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/a/img/@alt").get(default="no brand")
            product["lien_produit"]=article.xpath(".//div/div[@class='prdtBILImg']/a/@href").get()
            product["name"]=article.xpath(".//div/div[@class='prdtBILDetails']/div[contains(@class,'details product-item-details')]/strong/a/text()").get()
            product["image_url"]=article.xpath(".//div/div[@class='prdtBILImg']/a/span/span/img/@src").get()
            product["discount"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/div[@class='price-box price-final_price']/span[@class='discount-price']/text()").get(default="N/A")
            product["stock_availability"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/div[@class='card text-white bg-secondary mb-3 ']/div[@class='card-body']/div/span/text()").get()
            product["category"]=response.xpath("//div[@class='page-title-wrapper']/h1/span/text()").get()
            product["regular_price"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/div[@class='price-box price-final_price']/span[@class='old-price']/span[@class='price-container price-final_price tax']/span[@class='price-wrapper ']/span/text()").get(default="N/A")
            if  product["regular_price"]=="N/A" :
                product["price"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/div[@class='price-box price-final_price']/span/span/span/text()").get()
            else :
                product["price"]=article.xpath(".//div/div[@class='testLp4x prdtBILCta']/div[@class='price-box price-final_price']/span[@class='special-price']/span/span[@class='price-wrapper ']/span/text()").get(default="lalalal")
            yield product
            next = response.xpath("//div[@class='pages']/ul/li[contains(@class,'item pages-item-next')]/a/@href").get(default="N/A")
            if next!="N/A":
                yield response.follow(next,self.parse_product)



      