import scrapy
from ..items import WoodsItem

class EarthwerksspiderSpider(scrapy.Spider):
    name = 'earthwerksSpider'
    allowed_domains = ['earthwerks.com']
    start_urls = ['http://earthwerks.com/']

    def parse(self, response):
        
        category_urls = ['https://earthwerks.com/Vinyl/CORE',
                        'https://earthwerks.com/Vinyl/Performance',
                        'https://earthwerks.com/Vinyl/Development',
                        'https://earthwerks.com/Wood/'
                        ]
        
        for cUrl in category_urls:
            
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        product_urls=response.xpath("//div[@class='masonry masonry-shop']/div/div/a/@href").extract()
        
        for purl in product_urls:
            if 'CORE' in purl: 
                yield scrapy.Request('https://earthwerks.com/Vinyl/' + purl, callback=self.parse_sku)
            elif 'Performance' in purl: 
                yield scrapy.Request('https://earthwerks.com/Vinyl/' + purl, callback=self.parse_sku)
            elif 'Development' in purl: 
                yield scrapy.Request('https://earthwerks.com/Vinyl/' + purl, callback=self.parse_sku)
            else:
                yield scrapy.Request('https://earthwerks.com/Wood/' + purl, callback=self.parse_sku)
                
    def parse_sku(self, response):

        skus =response.xpath("//div[@class='masonry__container masonry--animate masonry--active']/div")
        collection =  response.xpath("//div[@class='item__title']/h4/text()").extract_first() 
        
        for sku in skus:

            handle = sku.xpath(".//em/text()").extract_first()

            title =  collection + sku.xpath(".//h5/text()").extract_first()

                
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'earthwerks' + '-' + formattedcode
            product['vendor']= 'earthwerks'
        

            yield product

