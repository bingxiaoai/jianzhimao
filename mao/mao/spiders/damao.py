import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DamaoSpider(CrawlSpider):
    name = 'damao'
    allowed_domains = ['89ip.cn']
    start_urls = ['https://www.89ip.cn']

    rules = (

        Rule(LinkExtractor(allow=r'index_\d{1,2}}.html'), callback='parse_item',follow=True,),
        # Rule(LinkExtractor(allow=r'/\w+_zbx_0/'), callback='parse_item', follow=True),
    )



    def parse_item(self, response):
        print(response.url)
        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
