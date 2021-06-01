import scrapy
from ..items import WoodsItem

class KnoasflooringspiderSpider(scrapy.Spider):
    name = 'knoasflooringSpider'
    allowed_domains = ['knoasflooring.com']
    start_urls = ['http://knoasflooring.com/']

    custom_settings = {
        'ROBOTSTXT_OBEY': 'false',
    }
    
    def parse(self, response):
        category_urls=['https://knoasflooring.com/product/citi-collection/',
                   'https://knoasflooring.com/product/evoke-collection/',
                   'https://knoasflooring.com/product/memories-collection/',
                   'https://knoasflooring.com/product/modern-family-ii-collection/',
                   'https://knoasflooring.com/product-category/laminate-floors/',
                   'https://knoasflooring.com/product/19th-century-collection-laminate-floors/',
                    'https://knoasflooring.com/product/albion-collection-laminate-floors/',
                    'https://knoasflooring.com/product/cascade-collection-laminate-floors/',
                    'https://knoasflooring.com/product/european-collection-laminate-floors/',
                    'https://knoasflooring.com/product/in-2-the-wood-laminate-flooring/',
                    'https://knoasflooring.com/product/platinum-collection-laminate-floors/',
                    'https://knoasflooring.com/product/revolution-collection/',
                    'https://knoasflooring.com/product/western-traditions-laminate-floors/'
]

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products,headers=headers)
    
   
    
    def parse_products(self, response):
        all_skus = response.xpath("//ol[@class='flex-control-nav flex-control-thumbs']/li//img")
        print(all_skus)
        for sku in all_skus:
            print('------------------------------')
            print(sku)
            url = product
            
            titlecode = url.rsplit('/', 1)[-1]
            title = (titlecode.rsplit('-', 1)[0])
            print(title)
                
            product = WoodsItem()
            product['title']= title
            product['handle']= title
            product['formattedcode'] = 'knoasflooring' + '-' + title
            product['vendor']= 'knoasflooring'
        
    
            yield product
