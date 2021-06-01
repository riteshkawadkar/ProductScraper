import scrapy
from ..items import WoodsItem

class EleganzatilesspiderSpider(scrapy.Spider):
    name = 'eleganzatilesSpider'
    allowed_domains = ['eleganzatiles.com']
    start_urls = ['http://www.eleganzatiles.com/product-series/spc/spc-flooring.html/']

    def parse(self, response):
        all_products=response.xpath("//div[@class='series-products']/div/div")
        
        for product in all_products:
            title = product.xpath(".//h3/text()").extract_first()
            handle = product.xpath(".//div[contains(@style,'padding')]/text()").extract_first().replace('SKU: ','')
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'eleganzatiles' + '-' + formattedcode
            product['vendor']= 'eleganzatiles'
           
      
            yield product
