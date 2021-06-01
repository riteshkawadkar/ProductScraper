import scrapy
from ..items import WoodsItem


class FuzionflooringspiderSpider(scrapy.Spider):
    name = 'fuzionflooringSpider'
    allowed_domains = ['fuzionflooring.com']
    start_urls = ['https://www.fuzionflooring.com/product-category/engineered-hardwood/']

    def parse(self, response):
        category_urls = ['https://www.fuzionflooring.com/product-category/engineered-hardwood/',
                        'https://www.fuzionflooring.com/product-category/luxury-vinyl/']
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//ul[@class='products columns-3']/li")
        
        for product in all_products:
            handle = product.xpath(".//header/span/text()").extract_first()
            a =  ((response.xpath("//h1[@class='fuzion-title space-b--lg']/text()").extract_first()).replace('Engineered ','')).replace('Luxury ','') 
            b =  product.xpath(".//header/h2/text()").extract_first() 
            c =  product.xpath(".//ul/li[1]/text()").extract_first().replace('Collection: ','')
            title = a  + " " + b  + " " + handle  + " " + c
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'fuzionflooring' + '-' + formattedcode
            product['vendor']= 'fuzionflooring'
           
      
            yield product
        
