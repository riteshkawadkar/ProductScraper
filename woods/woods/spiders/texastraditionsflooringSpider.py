import scrapy
from ..items import WoodsItem
import requests
from bs4 import BeautifulSoup

class TexastraditionsflooringspiderSpider(scrapy.Spider):
    name = 'texastraditionsflooringSpider'
    allowed_domains = ['texastraditionsflooring.com']
    start_urls = ['https://texastraditionsflooring.com/colors/']

    def parse(self, response):
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        page = requests.get('https://texastraditionsflooring.com/colors/', headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        #title_elem = soup.find_all('li', {'class': re.compile(r'product-type-simple$')})
        title_elem = soup.find_all('div', class_='ld-sp-info')
        for a in title_elem:
            sku = a.find('a').text


            product = WoodsItem()
            product['title']= sku 
            product['handle']= sku
            product['formattedcode'] = 'texastraditionsflooring' + '-' + sku
            product['vendor']= 'texastraditionsflooring'
            
        
            yield product
