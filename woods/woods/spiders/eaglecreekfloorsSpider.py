import scrapy
from ..items import WoodsItem

class EaglecreekfloorsspiderSpider(scrapy.Spider):
    name = 'eaglecreekfloorsSpider'
    allowed_domains = ['eaglecreekfloors.com']
    start_urls = ['http://eaglecreekfloors.com/']

    def parse(self, response):
        category_url = 'https://eaglecreekfloors.com/products/'
                
        yield scrapy.Request(category_url, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[starts-with(@class, 'woocommerce')]/div/div[not(@class='clear')]")

        for product in all_products:
            try:
                handle = product.xpath(".//h3[@class='woocommerce-loop-product__title']/text()").extract_first()
            except:
                handle=""
            
            try:
                a = product.xpath(".//div[@class='woo-cats']/span/a[1]/text()").extract_first()
            except:
                a=""
            
            try:
                b= product.xpath(".//div[@class='woo-cats']/span/a[2]/text()").extract_first()
            except:
                b=""
                
            if handle is None:
                handle=""
            if a is None:
                a=""    
            if b is None:
                b=""
                
            title = handle + " " + a + " " + b
            formattedcode = handle

                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'eaglecreekfloors' + '-' + formattedcode
            product['vendor']= 'eaglecreekfloors'
           
      
            yield product

