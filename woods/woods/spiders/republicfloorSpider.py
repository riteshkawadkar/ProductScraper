import scrapy
import re
from ..items import WoodsItem
            
class RepublicFloorSpider(scrapy.Spider):
    name = 'realwoodfloorsSpider'
    allowed_domains = ['republicfloor.com']
    start_urls = ['http://republicfloor.com']


    custom_settings = {'FEED_URI': 'woods/outputfile.json', 'CLOSESPIDER_TIMEOUT' : 90} # This will tell scrapy to store the scraped data to outputfile.json and for how long the spider should run.


    #get category urls from notebook
    def parse(self, response):
        category_urls = ['https://www.republicfloor.com/great-california-oak',
            'https://www.republicfloor.com/mountain-oak',
            'https://www.republicfloor.com/great-oregon-oak',
            'https://www.republicfloor.com/coastal-oak',
            'https://www.republicfloor.com/the-french-island',
            'https://www.republicfloor.com/beach-house',
            'https://www.republicfloor.com/countryside',
            'https://www.republicfloor.com/crown-colony',
            'https://www.republicfloor.com/carmel-by-the-sea',
            'https://www.republicfloor.com/southern-charm',
            'https://www.republicfloor.com/western-north-woods',
            'https://www.republicfloor.com/copy-of-clovercreek',
            'https://www.republicfloor.com/lion-meadows',
            'https://www.republicfloor.com/lion-creek',
            'https://www.republicfloor.com/clare-valley',
            'https://www.republicfloor.com/blackwater-canyon-collection',
            'https://www.republicfloor.com/glacier-point',
            'https://www.republicfloor.com/clovercreek',
            'https://www.republicfloor.com/big-cypress-collection',
            'https://www.republicfloor.com/walunthills-collection',
            'https://www.republicfloor.com/the-woodland-oak',
            'https://www.republicfloor.com/the-pacific-oak',
            'https://www.republicfloor.com/nature-stone',
            'https://www.republicfloor.com/copy-of-lion-meadows-collection-1',
            'https://www.republicfloor.com/frontier-collection',
            'https://www.republicfloor.com/european-collection',
            'https://www.republicfloor.com/european-plus-collection',
            'https://www.republicfloor.com/european-lite-collection',
            'https://www.republicfloor.com/the-french-riviera',
            'https://www.republicfloor.com/american-cavalier',
            'https://www.republicfloor.com/fortress-collection',
            'https://www.republicfloor.com/fortress-random-length',
            'https://www.republicfloor.com/the-glens-12mm',
            'https://www.republicfloor.com/big-oak-collection',
            'https://www.republicfloor.com/urbanica-82mm',
            'https://www.republicfloor.com/urbanica-12mm']
            
        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_products)
    
    def parse_products(self, response):
        all_products=response.xpath("//div[@data-testid='matrix-gallery-items-container']/div")

        for product in all_products:
            handle = product.xpath(".//following-sibling::p/text()").extract_first()
            title = product.xpath(".//div[@data-testid='gallery-item-title']/text()").extract_first()
            formattedcode = "TEST"

            pattern = r'(RE)[A-Z]*[-]*[0-9]*'
            sequence = title
            
            try:
                if handle is None:
                    formattedcode = re.search(pattern, sequence).group()
                elif 'Length' in handle:
                    formattedcode = re.search(pattern, sequence).group()
                else:
                    formattedcode = handle
            except AttributeError:
                formattedcode = 'NA'   
                
            product = WoodsItem()
            product['title']= title
            product['handle']= handle
            product['formattedcode'] = 'republicfloor' + '-' + formattedcode
            product['vendor']= 'republicfloor'
           
      
            yield product

    
    