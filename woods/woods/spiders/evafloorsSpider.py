import scrapy
from ..items import WoodsItem

class EvafloorsspiderSpider(scrapy.Spider):
    name = 'evafloorsSpider'
    allowed_domains = ['evafloors.com']
    start_urls = ['http://evafloors.com/']

    def parse(self, response):
        
        category_urls = ['https://evafloors.com/product-category/vinyl-water-proof/diamond-collection/',
                        'https://evafloors.com/product-category/vinyl-water-proof/spc/',
                        'https://evafloors.com/product-category/vinyl-water-proof/spc-vinyl-water-proof/',
                        'https://evafloors.com/product-category/laminate/water-resistant/',
                        'https://evafloors.com/product-category/engineered/wire-brushed-engineered/',
                        'https://evafloors.com/product-category/engineered/hand-scraped-engineered/',
                        'https://evafloors.com/product-category/engineered/smooth-engineered/'
                        ]
        
        for cUrl in category_urls:
            
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[starts-with(@class, 'woocommerce')]/ul/li/a")

        for product in all_products:
            try:
                handle = response.xpath(".//h2/text()").extract_first().split(' – ')[0]
            except:
                handle = response.xpath(".//h2/text()").extract_first()
                
            title =  response.xpath(".//h2/text()").extract_first().replace(' – ','-')

                
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'evafloors' + '-' + formattedcode
            product['vendor']= 'evafloors'
        

            yield product

