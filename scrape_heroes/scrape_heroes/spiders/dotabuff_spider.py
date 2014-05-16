from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrape_heroes.items import HeroItem


class DotaBuffSpider(CrawlSpider):
    name = 'scrape_heroes'
    allowed_domains = ['dotabuff.com']
    start_urls = ['http://www.dotabuff.com/heroes']
    rules = [Rule(SgmlLinkExtractor(allow=['/heroes/\w+']), 'parse_hero')]

    def parse_hero(self, response):
        selector = Selector(response)
        hero = HeroItem()
        hero['url'] = response.url
        hero['name'] = selector.xpath('//*[@id="content-header-primary"]/div[2]/h1/text()').extract()
        return hero
