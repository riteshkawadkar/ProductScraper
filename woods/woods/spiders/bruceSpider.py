import scrapy
import json
from ..items import WoodsItem

class BrucespiderSpider(scrapy.Spider):
    name = 'bruceSpider'
    allowed_domains = ['bruce.com']
    start_urls = ['http://bruce.com/']

    def parse(self, response):
        url = 'https://www.bruce.com/api/en-us/browse/products?filters=construction%3AEngineered+Hardwood&filters=construction%3ASolid+Hardwood&filters=construction%3ARigid+Core&size=1000'
        yield scrapy.Request(url, callback=self.parse_json)
        
    def parse_json(self, response):
        json_response  = json.loads(response.text)
        products = json_response["products"]
        
        for p in products:

            product = WoodsItem()
            product['title']= p["altName"] 
            product['handle']= p["line4"] 
            product['formattedcode'] = 'bruce' + '-' + p["line4"] 
            product['vendor']= 'bruce'
            
            yield product
            
        