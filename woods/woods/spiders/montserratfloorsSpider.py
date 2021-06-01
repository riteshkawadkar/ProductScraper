import scrapy
from ..items import WoodsItem

class MontserratfloorsspiderSpider(scrapy.Spider):
    name = 'montserratfloorsSpider'
    allowed_domains = ['montserratfloors.com']
    start_urls = ['http://montserratfloors.com/']

    def parse(self, response):
        category_urls = ['https://www.montserratfloors.com/engineered',
                        'https://www.montserratfloors.com/laminate',
                        'https://www.montserratfloors.com/wpc',
                        'https://www.montserratfloors.com/spc'
                        ]
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@id='projectThumbs']/div/a")
        category = response.xpath("//div[@class='sqs-block-content']/h2/text()").extract_first()
        
        for product in all_products:
            handle = product.xpath(".//div[@class='project-title']/text()").extract_first() 
            title =  category + " "  + handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'montserratfloors' + '-' + formattedcode
            product['vendor']= 'montserratfloors'
           
      
            yield product

