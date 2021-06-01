import scrapy
from ..items import WoodsItem

class TropicalflooringspiderSpider(scrapy.Spider):
    name = 'tropicalflooringSpider'
    allowed_domains = ['tropicalflooring.net']
    start_urls = ['http://tropicalflooring.net/']

    def parse(self, response):
        category_urls = ['https://www.tropicalflooring.net/solid-hardwood-1',
                        'https://www.tropicalflooring.net/engineered-hardwood',
                        'https://www.tropicalflooring.net/laminate',
                        'https://www.tropicalflooring.net/spc-flooring',
                        'https://www.tropicalflooring.net/wpc',
                        'https://www.tropicalflooring.net/lvt',
                        ]
        
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@id='productList']/a")
        
        for product in all_products:
            handle = product.xpath(".//div[@class='product-title']/text()").extract_first()
            title = product.xpath("//li[@class='nav-section-label']/text()").extract_first()  + " "  + handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'tropicalflooring' + '-' + formattedcode
            product['vendor']= 'tropicalflooring'
           
      
            yield product
