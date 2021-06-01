import scrapy
from ..items import WoodsItem

class ValenciahardwoodsspiderSpider(scrapy.Spider):
    name = 'valenciahardwoodsSpider'
    allowed_domains = ['valenciahardwoods.com']
    start_urls = ['https://valenciahardwoods.com/']

    def parse(self, response):
        
        category_urls = ['https://valenciahardwoods.com/floorartcollection',
                        'https://valenciahardwoods.com/european-wood-collection',
                        'https://valenciahardwoods.com/unfinished-collection'
                        ]
        
        for cUrl in category_urls:
            
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        product_urls=response.xpath("//div[@id='productList']/a/@href").extract()

        for purl in product_urls:
            yield scrapy.Request('https://valenciahardwoods.com' + purl, callback=self.parse_sku)
            
    def parse_sku(self, response):


        handle = response.xpath("//div[@class='sqs-block-content']/p[2]/text()").extract_first().replace(': ', '').replace('\xa0', '')

        title =  response.xpath("//h1[@class='page-title']/text()").extract_first() 

            
        formattedcode = handle
            
        product = WoodsItem()
        product['title']= title
        product['handle']= handle
        product['formattedcode'] = 'valenciahardwoods' + '-' + formattedcode
        product['vendor']= 'valenciahardwoods'
    

        yield product
