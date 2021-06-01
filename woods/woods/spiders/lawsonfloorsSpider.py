import scrapy
from ..items import WoodsItem

class LawsonfloorsspiderSpider(scrapy.Spider):
    name = 'lawsonfloorsSpider'
    allowed_domains = ['lawsonfloors.com']
    start_urls = ['https://lawsonfloors.com/']

    def parse(self, response):
        category_urls = ['https://lawsonfloors.com/portfolio-view/crown-premium-collection/',
                            'https://lawsonfloors.com/portfolio-view/dream-collection/',
                            'https://lawsonfloors.com/portfolio-view/heritage-collection/',
                            'https://lawsonfloors.com/portfolio-view/ranch-collection/',
                            'https://lawsonfloors.com/portfolio-view/royal-collection-25-year-warranty/',
                            'https://lawsonfloors.com/portfolio-view/destinations-collection/',
                            'https://lawsonfloors.com/portfolio-view/hermosa-collection/',
                            'https://lawsonfloors.com/portfolio-view/spc-flooring/',
                            'https://lawsonfloors.com/portfolio-view/vintage-collection/',
                            'https://lawsonfloors.com/portfolio-view/legends-collection-ii-spc-flooring/',
                            'https://lawsonfloors.com/portfolio-view/texas-living-collection/',
                            'https://lawsonfloors.com/portfolio-view/legends-collection-iii/']
        

        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_product)

            
    def parse_product(self, response):
        print(response.url)
        all_products = response.xpath("//div[@class='content-portfolio']/div")
        title = response.xpath("//article/h1/text()").extract_first().strip()

        for product in all_products: 

            handle = product.xpath(".//div[@class='title-portfolio']/span/text()").extract_first().strip()
            formattedcode = handle

            product = WoodsItem()
            product['title']= title + " " + handle
            product['handle']= handle
            product['formattedcode'] = 'lawsonfloors' + '-' + handle.split(' ')[0]
            product['vendor']= 'lawsonfloors'
           
      
            yield product


               
