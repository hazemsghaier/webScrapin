# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from SSR_DATA_COLLECTION.utilitis.proxy_manegment import Proxy
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time


class SsrDataCollectionSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SsrDataCollectionDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
from random import randint
from urllib.parse import urlencode
import requests
import logging
class spiderFakeHeadersMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def __init__(self,settings) :
        self.api_key=settings.get("SCRAPOPS_API_KEY")
        self.end_point=settings.get("SCRAPOPS_ENDPOINT")
        self.num_request=settings.get("NUMBER_OF_REQUEST")
        self.header_list={}
        self.header_list_from_scrapops=[]
        self.valid_header=False
        self.proxy_activated=False
        self.get_headers_list()
    def get_random_proxy(self):
        proxy=Proxy()
        return proxy.get_random_proxy()
           

    def get_headers_list(self):
        payload={
            'api_key': 'b3eea763-e6d4-4f13-8fab-61e9a7647ff8',

        }
        if self.num_request is not None:
            payload["num_results"]=self.num_request

            
        response=requests.get(self.end_point,params=urlencode(payload))
        
        json_response=response.json()
        self.header_list_from_scrapops=json_response.get("result",[])
    def get_random_header(self):
        random_index=randint(0,len(self.header_list_from_scrapops)-1)
           
        return self.header_list_from_scrapops[random_index] 
    def process_request(self,request,spider):
        if self.proxy_activated == True :
            request.meta["proxy"]="http://"+self.get_random_proxy()
        if self.valid_header==False:
            random_header=self.get_random_header()
            self.header_list=random_header
            request.headers["upgrade-insecure-requests"]=random_header["upgrade-insecure-requests"]
            request.headers["user-agent"]=random_header["user-agent"]
            request.headers["accept"]=random_header["accept"]
            request.headers["sec-ch-ua"]=random_header["sec-ch-ua"]
            request.headers["sec-ch-ua-mobile"]=random_header["sec-ch-ua-mobile"]
            request.headers["sec-ch-ua-platform"]=random_header["sec-ch-ua-platform"]
            request.headers["sec-fetch-site"]=random_header["sec-fetch-site"]
            request.headers["sec-fetch-mod"]=random_header["sec-fetch-mod"]
            request.headers["sec-fetch-user"]=random_header["sec-fetch-user"]
            request.headers["accept-language"]=random_header["accept-language"]
            request.headers["accept-encoding"]=random_header["accept-encoding"]

        else:    
            request.headers["upgrade-insecure-requests"]=self.header_list["upgrade-insecure-requests"]
            request.headers["user-agent"]=self.header_list["user-agent"]
            request.headers["accept"]=self.header_list["accept"]
            request.headers["sec-ch-ua"]=self.header_list["sec-ch-ua"]
            request.headers["sec-ch-ua-mobile"]=self.header_list["sec-ch-ua-mobile"]
            request.headers["sec-ch-ua-platform"]=self.header_list["sec-ch-ua-platform"]
            request.headers["sec-fetch-site"]=self.header_list["sec-fetch-site"]
            request.headers["sec-fetch-mod"]=self.header_list["sec-fetch-mod"]
            request.headers["sec-fetch-user"]=self.header_list["sec-fetch-user"]
            request.headers["accept-language"]=self.header_list["accept-language"]
            request.headers["accept-encoding"]=self.header_list["accept-encoding"]

       

    def process_response(self,request,response,spider)    :
        if response.status !=200 :
            time.sleep(0.5)
            logging.warning(f"the response status is {response.status}:we resend the request to {request.url} for  time")
            return request
        self.valid_header=True

        return response
    def process_exception(self, request, exception, spider):
        logging.error(f'Proxy failed: {exception}')  
        print("we have some problems ")  
        
