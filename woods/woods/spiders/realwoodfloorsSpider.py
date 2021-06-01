import scrapy
from ..items import WoodsItem

class RealwoodfloorsspiderSpider(scrapy.Spider):
    name = 'realwoodfloorsSpider'
    allowed_domains = ['realwoodfloors.com']
    start_urls = ['https://realwoodfloors.com/collections/sort']

    def parse(self, response):
        all_products = response.xpath("//div[@class='modal product-modal modal-fixed-footer']")


        for p in all_products: 
            title = p.xpath(".//self::div/@id").extract_first()
            handle = p.xpath(".//self::div/@id").extract_first()
            formattedcode = handle

            product = WoodsItem()
            product['title']= title 
            product['handle']= handle
            product['formattedcode'] = 'realwoodfloors' + '-' + handle
            product['vendor']= 'realwoodfloors'
           
      
            yield product
        
