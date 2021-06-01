import scrapy
from ..items import WoodsItem

class JohnsonHardwoodspiderSpider(scrapy.Spider):
    name = 'johnsonhardwoodspider'
    allowed_domains = ['johnsonhardwood.com']
    start_urls = ['https://johnsonhardwood.com//']

    def parse(self, response):
        #get list of urls for proucts
        category_urls=response.xpath("//li[2]/ul/li/a/@href").extract()
        #print('---------------------------------------------------------------------------------------------')
        #print(category_urls)
        
        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_product)
        
    def parse_product(self, response):
        all_products = response.xpath("//div[@class='products']/a")
        
        for product in all_products:
            title = product.xpath(".//div[@class='header-wrapper']/h1/text()").extract_first()
            code = product.xpath(".//div[@class='header-wrapper']/span[@class='num']/text()").extract_first()
            formattedcode = code

            product = WoodsItem()
            product['title']= title
            product['handle']= code
            product['formattedcode'] = 'johnsonhardwood' + '-' + formattedcode
            product['vendor']='johnsonhardwood'
            
           
      
            yield product

