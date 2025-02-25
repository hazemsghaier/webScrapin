from typing import Any
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_headers import Headers
import time
import datetime
from SSR_DATA_COLLECTION.items import JumiaProduct

class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["www.jumia.com.tn"]
    start_urls = ["https://www.jumia.com.tn/"]

    def __init__(self):
        self.file=open(r"C:\Users\PCS\Desktop\data_collection\data-collection\SSR_DATA_COLLECTION\SSR_DATA_COLLECTION\static\log.txt","w",encoding="utf-8")
        super().__init__()
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        articles = response.css("article.prd")
        list_des_lien_a_visiter = []

        for article in articles:
            href = article.css("a.core::attr(href)").get()
            if href:
                list_des_lien_a_visiter.append(href)
            item=JumiaProduct()    
            item["price"]=article.css(".prc::text").get(default="N/A")
            item["name"]=article.css(".name::text").get(default="N/A")
            item["discount"]=article.css(".dsct::text").get(default="N/A")
            item["nombre_des_article_restent"]= article.css(".stk::text").get(default="N/A")
            item["prix_precedent"]=article.css(".prc::attr(data-oprc)").get(default="N/A")
            item["image_url"]=article.css("img::attr(data-src)").get(default="N/A")
            item["brand"]=article.css("a::attr(data-gtm-brand)").get(default="N/A")
            item["categorie"]=article.css("a::attr(data-gtm-category)").get(default="N/A")
            item["product_page_link"]=article.css("a.core::attr(href)").get(default="N/A")
            yield item

        self.driver.get(response.url)
        self.driver.implicitly_wait(5)
        time.sleep(0.5)

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.s-itm[role=menuitem]')
        hrefs = [element.get_attribute('href') for element in elements]
        
        for href in hrefs:

           # self.file.write(str(href) + "\n")

            if href:
               yield response.follow(href, callback=self.parse_catalogue)

    def parse_catalogue(self, response):
        articles = response.xpath("//article[@class='prd _fb col c-prd']")

        for article in articles:
            item=JumiaProduct()
            item["price"]=article.css("div.prc::text").get(default="N/A")
            item["name"]=article.css("div").css("h3.name::text").get(default="N/A")
            item["discount"]=article.css("div.bdg._dsct::text").get(default="N/A")
            item["nombre_des_article_restent"]= article.css(".stk::text").get(default="N/A")
            item["prix_precedent"]=article.css(".old::text").get(default="N/A")
            item["image_url"]=article.css("img::attr(data-src)").get(default="N/A")
            item["brand"]=article.css("a::attr(data-gtm-brand)").get(default="N/A")
            item["categorie"]=article.css("a::attr(data-gtm-category)").get(default="N/A")
            item["product_page_link"]=article.xpath(".//a[@class='core']/@href").get(default="N/A")
            page=response.urljoin(item["product_page_link"])
            item["product_page_link"]=page
            yield response.follow(page,self.parse_product_page,meta={'item': item})
         
        
        
        next_page = response.xpath("//a[@aria-label='Page suivante']/@href").get(default="vide")
        
        if next_page != "vide":
            next_page = response.urljoin(next_page)
            if next_page=="https://www.jumia.com.tn/customer/account/login/?tkWl=ME403FD0AOIQWNAFAMZ-308485&return=%2Fmlp-boutique-metaltex%2F%3Fpage%3D2":
                print("1111111111111111111111111111")
            yield response.follow(next_page, callback=self.parse_catalogue)
        else:
            self.file.write("JUMIA:No next page found. Scraping completed.\n")
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
    def parse_product_page(self,response):
        item=response.meta["item"]
        item["description"]=response.xpath("normalize-space(//div[@class='card aim -mtm'])").get(default="N/Ammm")
        return item
