import scrapy
import requests
from bs4 import BeautifulSoup
from ..items import WoodsItem


class LwflooringspiderSpider(scrapy.Spider):
    name = 'lwflooringSpider'
    allowed_domains = ['lwflooring.com']
    start_urls = ['http://www.lwflooring.com/']
    
    def parse(self, response):
        url = 'http://www.lwflooring.com/sitemap_0.xml'
        yield scrapy.Request(url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        
        page = requests.get(response.url)
        #print('----------------------------------------------------------------------')

        soup = BeautifulSoup(page.text, 'html.parser')
        
        products = soup.find_all('loc')
        
        
        for link in products:
            print(link.text)
            if ('evp' in link.text) or ('wood-flooring' in link.text):
          
                titlecode = link.text.rsplit('/', 1)[-1]
                title = (titlecode.rsplit('-', 1)[0])
                code = (titlecode.rsplit('-', 1)[1])
                formattedcode = code
 
                yield {
                    'title': title, 
                    'code': code, 
                    'formattedcode':'lwflooring' + '-' + formattedcode, 
                    'vendor':'lwflooring' 
                    }  
       
