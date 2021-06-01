import scrapy
import requests
from bs4 import BeautifulSoup
from ..items import WoodsItem

class BpiprestigespiderSpider(scrapy.Spider):
    name = 'bpiprestigeSpider'
    allowed_domains = ['bpiprestige.com']
    start_urls = ['https://bpiprestige.com/sitemap_products_1.xml?from=1884948988000&to=6696567242917']

    def parse(self, response):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

        url = 'https://bpiprestige.com/sitemap_products_1.xml?from=1884948988000&to=6696567242917'
        yield scrapy.Request(url, callback=self.parse_sitemap, headers=headers)

    def parse_sitemap(self, response):
        page = requests.get(response.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        products = soup.find_all('loc')

        
        for link in products:
            if ('/products/' in link.text):
                #print('---------------------------------------------------')
                #print(link.text)
                yield scrapy.Request(link.text, callback=self.parse_products)
            
    def parse_products(self, response):
        #print(response.url)
        all_products=response.xpath("//div[@class='collection-grid']//div[@class='product-details']")
        
        for product in all_products:
            handle = product.xpath(".//h4[3]/text()").extract_first().replace('Item Number: ','')
            collection_name = product.xpath(".//h4[1]/text()").extract_first().replace('Collection: ','')
            color_name = product.xpath(".//h4[2]/text()").extract_first().replace('Color: ','')
            product_name =  product.xpath("//div[@class='meta-options']//a[1]/text()").extract_first()
            title = product_name  + " " + collection_name  + " " + color_name  + " " + handle
            formattedcode = handle
                
            if not formattedcode:
                pass
            else:
                product = WoodsItem()
                product['title']= title
                product['handle']= handle
                product['formattedcode'] = 'bpiprestige' + '-' + formattedcode
                product['vendor']= 'bpiprestige'
           
      
            yield product
            
