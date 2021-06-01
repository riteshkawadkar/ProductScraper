import scrapy
from ..items import WoodsItem

class AayersfloorsspiderSpider(scrapy.Spider):
    name = 'aayersfloorsSpider'
    allowed_domains = ['aayersfloors.com']
    start_urls = ['http://aayersfloors.com/index.php/home/product/index/pid/59.html']

    def parse(self, response):
        category_urls = ['http://aayersfloors.com/index.php/home/product/index/pid/59.html',
                        'http://aayersfloors.com/index.php/home/product/index/pid/57.html',
                        'http://aayersfloors.com/index.php/home/product/index/pid/55.html',
                        'http://aayersfloors.com/index.php/home/product/index/pid/16.html'
                        ]
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@class='t_1140_5']/ul/li/div[@class='tit_pro2']")
        category = response.xpath("//div[@class='tit_6']/text()").extract_first()
        
        for product in all_products:
            handle = product.xpath(".//a/text()").extract_first() 
            title =  category + " "  + handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'aayersfloors' + '-' + formattedcode
            product['vendor']= 'aayersfloors'
           
      
            yield product

