import scrapy
from ..items import WoodsItem

class SlccflooringspiderSpider(scrapy.Spider):
    name = 'slccflooringSpider'
    allowed_domains = ['slccflooring.com']
    start_urls = ['https://www.slccflooring.com/products?page=1']

    def parse(self, response):
        category_url = 'https://www.slccflooring.com/products?page='
        
        for i in range(7):
            cUrl = category_url + str(i)
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@class='view-content']/div")
        
        for product in all_products:
            handle = product.xpath(".//span[@class='field-content']/a/text()").extract_first()
            title = handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'slccflooring' + '-' + formattedcode
            product['vendor']= 'slccflooring'
           
      
            yield product

