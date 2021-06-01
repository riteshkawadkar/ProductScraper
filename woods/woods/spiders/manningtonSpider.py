import scrapy
from ..items import WoodsItem

class ManningtonspiderSpider(scrapy.Spider):
    name = 'manningtonSpider'
    allowed_domains = ['mannington.com']
    start_urls = ['https://mannington.com/']

    def parse(self, response):
        category_urls = ['https://www.mannington.com/Residential/Adura-Vinyl-Plank/AduraMaxApex/Search',
                        'https://www.mannington.com/Residential/Adura-Vinyl-Plank/AduraMax/Search',
                        'https://www.mannington.com/Residential/Adura-Vinyl-Plank/AduraRigid/Search',
                        'https://www.mannington.com/Residential/Adura-Vinyl-Plank/AduraFlex/Search',
                        'https://www.mannington.com/Residential/Hardwood/Search',
                        'https://www.mannington.com/Residential/Laminate/Search',
                        'https://www.mannington.com/Residential/VinylSheet/LuxuryVinylSheet/Search',
                        'https://www.mannington.com/Residential/VinylSheet/Resilient/Search'
                        ]
                
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@class='product-thumbs']/div")

        for product in all_products:
            handle = product.xpath(".//a/@href").extract_first().split('/')[-1]
            title = product.xpath(".//span[1]/text()").extract_first() + " " + product.xpath(".//span[2]/text()").extract_first() + " " + product.xpath(".//span[2]/text()").extract_first()
            formattedcode = handle

                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'mannington' + '-' + formattedcode
            product['vendor']= 'mannington'
           
      
            yield product
