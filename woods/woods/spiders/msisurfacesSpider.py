import scrapy
import requests
from bs4 import BeautifulSoup
from ..items import WoodsItem

from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

class MsisurfacesspiderSpider(scrapy.Spider):
    name = 'msisurfacesSpider'
    allowed_domains = ['msisurfaces.com']
    start_urls = ['https://www.msisurfaces.com/sitemap.xml']

    
    def parse(self, response):
        url = 'https://www.msisurfaces.com/sitemap.xml'
        yield scrapy.Request(url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        
        page = requests.get(response.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        products = soup.find_all('loc')

        
        for link in products:
            if ('/vinyl-flooring/' in link.text):
                print(link.text)
                try:
                    title = PurePosixPath(
                        unquote(
                            urlparse(
                                link.text
                            ).path
                        )
                    ).parts[2]
                    print(title)
                    code = PurePosixPath(
                        unquote(
                            urlparse(
                                link.text
                            ).path
                        )
                    ).parts[3]
                    formattedcode = code
                    
                    yield {
                        'title': title, 
                        'code': code, 
                        'formattedcode':'msisurfaces' + '-' + formattedcode, 
                        'vendor':'msisurfaces' }  
                except:
                    pass
 
                
       
