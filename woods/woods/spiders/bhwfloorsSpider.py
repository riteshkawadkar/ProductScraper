import scrapy
from ..items import WoodsItem
import requests
from bs4 import BeautifulSoup

class BhwfloorsspiderSpider(scrapy.Spider):
    name = 'bhwfloorsSpider'
    allowed_domains = ['bhwfloors.com']
    start_urls = ['https://bhwfloors.com/products.html']

    
    custom_settings = {
        'ROBOTSTXT_OBEY': 'false',
    }
    def parse(self, response):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        page = requests.get('https://bhwfloors.com/products.html', headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        products = soup.select('.grid a')
        for a in products:

            pageP = requests.get('https://bhwfloors.com/' + a['href'])
            soupP = BeautifulSoup(pageP.text, 'html.parser')
            handle = soupP.find_all('h1')
            title = handle[0].getText()

            product = WoodsItem()
            product['title']= title
                
            product['handle']= title
            product['formattedcode'] = 'bhwfloors' + '-' + title
            product['vendor']= 'bhwfloors'
            
        
            yield product
    
    