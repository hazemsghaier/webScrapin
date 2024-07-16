import scrapy
from SSR_DATA_COLLECTION.items import TunisiaNetProduct


class TunisianetSpider(scrapy.Spider):
    name = "tunisiaNet"
    allowed_domains = ["www.tunisianet.com.tn"]
    start_urls = ["https://www.tunisianet.com.tn/301-pc-portable-tunisie"]

    def parse(self, response):
        categories = response.css(".menu-item.item-line a::attr(href)").getall()
        s = 0
        for i in categories:
            if s < 5:
                print("=======================================================-")
                yield response.follow(i, self.parse_product)
                s += 1
            else:
                print("22222222222222222222222222222")
                break
                 
          

    def parse_product(self, response):
        print("111111111111111111111111111111111111111111111111")
        articles = response.xpath("//article[contains(@class, 'product-miniature') and contains(@class, 'js-product-miniature')]")
        print(len(articles))
        if response.url=="https://www.tunisianet.com.tn/681-pc-portable-gamer" :
            for article in articles:
                print(response.url)

                tunisia_net=TunisiaNetProduct()
                tunisia_net["price"]=article.xpath(".//span[@itemprop='price']/text()").get(default="N/A")
                tunisia_net["description"]=article.css("div[id^='product-description-short-'] *::text").getall()
                tunisia_net["lien_produit"]=article.xpath(".//div[@itemprop='description']/a/@href").get(default="N/A")
                tunisia_net["name"]=article.css(".h3.product-title").css("a::text").get(default="N/A")
                tunisia_net["image_url"]=article.xpath(".//div[contains(@class, 'wb-image-block') and contains(@class, 'col-lg-3') and contains(@class, 'col-xl-3') and contains(@class, 'col-md-4') and contains(@class, 'col-sm-4') and contains(@class, 'col-xs-6')]/a/img[contains(@class, 'center')]/@src").get(default="N/A")
                tunisia_net["regular_price"]=article.xpath(".//span[@class='regular-price']/text()").get(default="N/A")
                tunisia_net["discount"]= article.css("span.discount-amount::text").get(default="N/A")
                tunisia_net["stock_availability"]=article.css("#stock_availability").css("span::text").get(default="N/A")
                yield tunisia_net
