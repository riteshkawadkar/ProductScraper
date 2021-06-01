import scrapy
from ..items import WoodsItem

class HillcountryinnovationsspiderSpider(scrapy.Spider):
    name = 'hillcountryinnovationsSpider'
    allowed_domains = ['hillcountryinnovations.com']
    start_urls = ['http://hillcountryinnovations.com/']

    def parse(self, response):
        all_categories=response.xpath("//ul[@id='menu-alt-menu']/li//ul//a/@href").extract()
        for link in all_categories:
            #print(link)
            yield scrapy.Request(link, callback=self.parse_products)
            
    def parse_products(self, response):
        try:
            collection_name = response.xpath("//h1[@class='title']/b/text()").extract_first()
        except:
            collection_name=""
        try:
            catgeory_name = response.xpath("//div[@class='inside']/p/text()").extract_first()
        except:
            catgeory_name=""
            
        all_products=response.xpath("//div[@class='bq_wrapper']")
        
        for p in all_products:
            product = WoodsItem()
            try:
                title = p.xpath(".//h3/text()").extract_first().repalce('\u00e9', 'é')
            except:
                title=""
                
            if (collection_name is None):
                collection_name = "Collection"
            elif (catgeory_name is None):
                catgeory_name="Category"
            elif (title is None):
                title="Title"
                
            handle = p.xpath(".//div[@class='bottom-product']//p/text()").extract_first().replace(' ', '')
            product['title']= catgeory_name + " " + collection_name + " " + title + " " + handle
            
            product['handle']= handle
            product['formattedcode'] = 'hillcountryinnovations' + '-' + handle
            product['vendor']= 'hillcountryinnovations'
           
      
            yield product
        
        
