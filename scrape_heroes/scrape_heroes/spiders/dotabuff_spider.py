from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrape_heroes.items import HeroItem
from selenium import webdriver
import time


class DotaBuffSpider(CrawlSpider):
    name = 'scrape_heroes'
    allowed_domains = ['dotabuff.com']
    start_urls = ['http://www.dotabuff.com/heroes']
    rules = [Rule(SgmlLinkExtractor(allow=['/heroes/\w+']), callback='parse_hero')]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def parse_hero(self, response):
        hero = HeroItem()
        hero['url'] = response.url

        """ dotabuff used JavaScript calls to generate the content dynamiclly, therefore
            we make the call using the browser and scrape the content from the broweser """
        self.browser.get(response.url)

        """ wait for the JavaScript to load the page """
        time.sleep(3)

        selector = Selector(text=self.browser.page_source)
        best_versus = []
        best_versus_table = selector.xpath('//*[@id="hero-versus"]/section[1]/article/table/tbody')

        for selected_hero in best_versus_table:
            best_versus.extend(selected_hero.xpath('.//*[@class="hero-link"]/text()').extract())

        hero['best_versus'] = best_versus
        hero['name'] = selector.xpath('//*[@id="content-header-primary"]/div[2]/h1/text()').extract()

        return hero
