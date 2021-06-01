import scrapy
from ..items import WoodsItem
import requests
from bs4 import BeautifulSoup

class IndusparquetspiderSpider(scrapy.Spider):
    name = 'indusparquetSpider'
    allowed_domains = ['indusparquet-usa.com']
    start_urls = ['http://indusparquet-usa.com/']

    def parse(self, response):
        
        category_urls = ['https://www.indusparquet-usa.com/collections/solido/',
                        'https://www.indusparquet-usa.com/collections/classico/',
                        'https://www.indusparquet-usa.com/collections/largo/',
                        'https://www.indusparquet-usa.com/collections/novo/',
                        'https://www.indusparquet-usa.com/collections/valor/'
                        ]
        
        for cUrl in category_urls:
            
            yield scrapy.Request(cUrl, callback=self.parse_products, encoding='utf-8')
    
    def parse_products(self, response):
        product_urls=response.xpath("//div[starts-with(@class,'woocommerce')]/ul/li/a/@href").extract()

        for purl in product_urls:
            yield scrapy.Request(purl, callback=self.parse_sku, encoding='utf-8')
            
    def parse_sku(self, response):

        try:
            #print(response.url)
            handle = response.xpath("//div[@class='wc-product-description']/p[2]/text()").extract_first()
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

            page = requests.get(response.url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')

            title_elem = soup.find('div', class_='wc-product-description')
            sku = title_elem.find_all('p')
            #print(sku)
            a = sku[1].text.strip()
            #print(a)
            b = a.replace('SKU: ', '')
            #print(b)
            c = b.split('|')[0]
            #print(c)
            handle = c.split('–')[1].strip()
            
            
        except:
            handle=response.xpath("//p[@class='mb-4']/text()").extract_first().strip()
            
        try:
            title =  response.xpath("//h1[@class='product_title entry-title']/text()").extract_first() 
        except:
            title = ""
            
        formattedcode = handle
            
        product = WoodsItem()
        product['title']= title
        product['handle']= handle
        product['formattedcode'] = 'indusparquet-usa' + '-' + formattedcode
        product['vendor']= 'indusparquet-usa'
    

        yield product

