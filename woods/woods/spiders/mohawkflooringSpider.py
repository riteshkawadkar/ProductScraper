import scrapy
import requests
from bs4 import BeautifulSoup
from ..items import WoodsItem
import json 

class MohawkflooringspiderSpider(scrapy.Spider):
    name = 'mohawkflooringSpider'
    allowed_domains = ['mohawkflooring.com']
    start_urls   = ['https://www.mohawkflooring.com']

    
    
    def parse(self, response):
        category_urls = ['https://www.mohawkflooring.com/api/products/sitemap/0',
                         'https://www.mohawkflooring.com/api/products/sitemap/1',
                        'https://www.mohawkflooring.com/api/products/sitemap/2']
        

        for cUrl in category_urls:
            yield scrapy.Request(cUrl, callback=self.parse_sitemap)

            
    def parse_sitemap(self, response):
        
        page = requests.get(response.url)
        #print(page)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        products = soup.find_all('loc')
        
        for link in products:
            if ('hardwood' in link.text) or ('luxury-vinyl-tile' in link.text) or ('laminate-wood' in link.text):
                #print(link.text)
                title = link.text.rsplit('/', 1)[-1]
                handle = (link.text.rsplit('/', 1)[0]).rsplit('/', 1)[1]
                formattedcode = ((title.replace('-', ' ')).replace('.', '')).replace('"', '')
                #product = WoodsItem()

                yield {
                    'title': title, 
                    'handle': handle, 
                    'formattedcode':'mohawkflooring' + '-' + formattedcode, 
                    'vendor':'mohawkflooring' }  
               
         
         
        
     

 
    
  