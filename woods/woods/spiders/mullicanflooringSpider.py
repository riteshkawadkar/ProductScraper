import scrapy
import json
from ..items import WoodsItem

class MullicanflooringspiderSpider(scrapy.Spider):
    name = 'mullicanflooringSpider'
    allowed_domains = ['mullicanflooring.com']
    start_urls = ['https://www.mullicanflooring.com/api/productListing/']

    def parse(self, response):
        base_url = 'https://www.mullicanflooring.com/api/productListing/'
        json_response  = json.loads(response.text)
        ProductCount = int(int(json_response["ProductCount"])/9)
        
        for count in range(ProductCount):
            url = base_url + str(count)
            yield scrapy.Request(url, callback=self.parse_json)
        
    def parse_json(self, response):        
        json_response  = json.loads(response.text)
        products = json_response["ProductListings"]
        
        for p in products:

            product = WoodsItem()
            product['title']= p["Collection"] + p["MarketingName"] + p["Sku"]
            product['handle']= p["Sku"]
            product['formattedcode'] = 'mullicanflooring' + '-' + p["Sku"]
            product['vendor']= 'mullicanflooring'
            
            yield product
