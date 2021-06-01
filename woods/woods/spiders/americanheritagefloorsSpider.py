import scrapy
from ..items import WoodsItem
import requests
from bs4 import BeautifulSoup

class AmericanheritagefloorsspiderSpider(scrapy.Spider):
    name = 'americanheritagefloorsSpider'
    allowed_domains = ['americanheritagefloors.com']
    start_urls = ['http://www.americanheritagefloors.com/the-floors']

    

    def parse(self, response):
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        page = requests.get('http://www.americanheritagefloors.com/the-floors/', headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')

        div_Title_elem = soup.find_all('div', class_='Index-nav-text')
        for a in div_Title_elem:
            sku = a.find('span').text

            product = WoodsItem()
            product['title']= sku 
            product['handle']= sku
            product['formattedcode'] = 'americanheritagefloors' + '-' + sku
            product['vendor']= 'americanheritagefloors'
            
        
            yield product