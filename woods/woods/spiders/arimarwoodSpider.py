import scrapy
from ..items import WoodsItem

class ArimarwoodspiderSpider(scrapy.Spider):
    name = 'arimarwoodSpider'
    allowed_domains = ['arimarwood.com']
    start_urls = ['https://www.arimarwood.com/floor-art-antique-wide-plank-collection/']

    def parse(self, response):
        category_urls = ['https://www.arimarwood.com/floor-art-antique-wide-plank-collection/',
                        'https://www.arimarwood.com/villa-collection/',
                        'https://www.arimarwood.com/old-world-collection/',
                        'https://www.arimarwood.com/fashion-collection/',
                        'https://www.arimarwood.com/exotic-tropical-collection/'
                        ]
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[starts-with(@class,'et_pb_row')]/div/div/a[not(@class)]/@href").extract()
        
        for product in all_products:
            print(product)
            handle = product.replace('https://www.arimarwood.com//', '').replace('https://www.arimarwood.com/', '')
            
                
            product = WoodsItem()
            product['title']= handle
            product['handle']= handle
            product['formattedcode'] = 'arimarwood' + '-' + handle
            product['vendor']= 'arimarwood'
           
      
            yield product
