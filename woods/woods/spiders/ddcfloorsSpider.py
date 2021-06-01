import scrapy
from ..items import WoodsItem

class DdcfloorsspiderSpider(scrapy.Spider):
    name = 'ddcfloorsSpider'
    allowed_domains = ['ddcfloors.com']
    start_urls = ['http://www.ddcfloors.com/']

    def parse(self, response):
        
        category_urls = ['http://www.ddcfloors.com/mountain.html',
                        'http://www.ddcfloors.com/mountain%20plus.html',
                        'http://www.ddcfloors.com/mountain%20prime.html',
                        'http://www.ddcfloors.com/loto%20tec.%20plus.html'
                        ]
        
        for cUrl in category_urls:
            
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        product_urls=response.xpath("//div[@class='container']//div[@class='col-md-4']//a/@href").extract()
        
        for purl in product_urls:
            yield scrapy.Request('http://www.ddcfloors.com' + purl, callback=self.parse_sku)

                
    def parse_sku(self, response):

        handle =response.xpath("//p/span/text()").extract_first() 
        title =  response.xpath("//div[@class='tc-box article-box']/h2/text()").extract_first()   
        formattedcode = handle
            
        product = WoodsItem()
        product['title']= title
        product['handle']= handle
        product['formattedcode'] = 'ddcfloors' + '-' + formattedcode
        product['vendor']= 'ddcfloors'
    

        yield product


