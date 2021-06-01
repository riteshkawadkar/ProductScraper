import scrapy
import json
from ..items import WoodsItem

class ShawfloorspiderSpider(scrapy.Spider):
    name = 'shawfloorSpider'
    allowed_domains = ['shawfloors.com']
    start_urls = ['https://shawfloors.com/']
    
    

    def parse(self, response):
        base_url = 'https://shawfloors.com/api/odata/'
        categories = ['Resilient',
                    'Hardwoods']
        
        
        for category in categories:
            category_url = base_url + category + '?$select=SellingStyleNbr,ColorCount&$orderby=SellingStyleNbr&$filter=(ColorCount%20gt%200)%20and%20(ProductGroupPermanentName%20eq%20%27shawfloors%27)%20and%20(ProductGroupShowOnBrowseCat%20eq%20true)%20and%20(IsDefaultStyleColor%20eq%20true)&$count=true'
            yield scrapy.Request(category_url, callback=self.parse_category)
            
    def parse_category(self, response):
        json_response  = json.loads(response.text)
        SellingStyleNbrs = json_response["value"]
        
        base_url = 'https://shawfloors.com/api/odata/'
        
        for value in SellingStyleNbrs:
            #print(response.url)
            #print(value["SellingStyleNbr"])
            #print(value["ColorCount"])
            product_url = response.url.split('?')[0]  + '?$filter=SellingStyleNbr%20eq%20%27' + value["SellingStyleNbr"] + '%27%20and%20IsDropped%20eq%20false%20and%20ProductGroupPermanentName%20eq%20%27shawfloors%27'
            print(product_url)
            yield scrapy.Request(product_url, callback=self.parse_product)
            
    def parse_product(self, response):
        json_response  = json.loads(response.text)
        SellingColorNames = json_response["value"]
        print(response.url)
        
        for color in SellingColorNames:
            print(color["SellingColorName"])
            print(color["UniqueId"])
            
            product = WoodsItem()
            product['title']= color["SellingColorName"]
            product['handle']= color["UniqueId"]
            product['formattedcode'] = 'shawfloors' + '-' + color["UniqueId"]
            product['vendor']= 'shawfloors'
           
      
            yield product
