import scrapy
from ..items import WoodsItem

class UniflooraquaspiderSpider(scrapy.Spider):
    name = 'uniflooraquaSpider'
    allowed_domains = ['uniflooraqua.com']
    start_urls = ['http://uniflooraqua.com/']

    def parse(self, response):
        category_url = ['https://www.uniflooraqua.com/perfection',
                        'https://www.uniflooraqua.com/sensation',
                        'https://www.uniflooraqua.com/victoryii',
                        'https://www.uniflooraqua.com/lozeta',
                        'https://www.uniflooraqua.com/duration',
                        'https://www.uniflooraqua.com/creation',
                        'https://www.uniflooraqua.com/classics',
                        ]
        for cUrl in category_url:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@class='-YTXd _2L1uK']/div")
        
        for product in all_products:
            handle = product.xpath(".//div[@data-testid='gallery-item-title']/text()").extract_first()
            title = handle
            formattedcode = handle
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'uniflooraqua' + '-' + formattedcode
            product['vendor']= 'uniflooraqua'
           
      
            yield product

