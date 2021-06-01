import scrapy
from ..items import WoodsItem

class LicousspiderSpider(scrapy.Spider):
    name = 'licousSpider'
    allowed_domains = ['lico-us.com']
    start_urls = ['http://lico-us.com/']

    def parse(self, response):
        category_urls = ['https://lico-us.com/hydrofix/hydro-fix-collection/',
                            'https://lico-us.com/micodur/micodur-collection/'
                            ]
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)

    def parse_products(self, response):
        all_products=response.xpath("//div[@id='gallery']/div")
        
        for product in all_products:
            title = product.xpath(".//a/h4/text()").extract_first()
            handle = product.xpath(".//a/h4/text()").extract_first()
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'lico-us' + '-' + formattedcode
            product['vendor']= 'lico-us'
           
      
            yield product