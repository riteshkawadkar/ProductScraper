import scrapy
from ..items import WoodsItem

class UrbanfloorspiderSpider(scrapy.Spider):
    name = 'urbanfloorSpider'
    allowed_domains = ['urbanfloor.com']
    start_urls = ['http://urbanfloor.com/']

    def parse(self, response):
        category_url = 'https://www.urbanfloor.com/All_products.html'
        yield scrapy.Request(category_url, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@class='p-index-main']/div[@class='container-fluid']/div[@class='row']/div")
        
        for product in all_products:
            handle = product.xpath(".//h3[2]/text()").extract_first()
            title = product.xpath(".//h3[1]/text()").extract_first() + handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'urbanfloor' + '-' + formattedcode
            product['vendor']= 'urbanfloor'
           
      
            yield product
