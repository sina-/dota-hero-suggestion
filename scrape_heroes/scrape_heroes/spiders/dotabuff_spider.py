from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrape_heroes.items import HeroItem
from selenium import webdriver

from itertools import izip
from collections import namedtuple
import time

Info = namedtuple('Info', 'advantage, win_rate, number_of_matches')


class DotaBuffSpider(CrawlSpider):
    name = 'scrape_heroes'
    allowed_domains = ['dotabuff.com']
    start_urls = ['http://www.dotabuff.com/heroes']
    rules = [Rule(SgmlLinkExtractor(allow=['/heroes/\w+'], 
                                    deny=['/heroes/played', '/heroes/winning', '/heroes/impact',
                                          '/heroes/economy', '/heroes/farm', '/heroes/damage']), 
                                        callback='parse_hero')]

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
        best_versus_hero = {}

        best_versus_table = selector.xpath('//*[@id="hero-versus"]/section[1]/article/table/tbody')

        """ notice the . in the beggining to force search in the local xpath rather than 
            global for "hero-link" class """
        hero_name = best_versus_table.xpath('.//*[@class="hero-link"]/text()').extract()
        hero_advantage = best_versus_table.xpath('.//tr[*]/td[3]/text()').extract()
        hero_win_rate = best_versus_table.xpath('.//tr[*]/td[4]/text()').extract()
        hero_number_of_matches = best_versus_table.xpath('.//tr[*]/td[5]/text()').extract()

        for hn, ha, hwr, hnom in izip(hero_name, hero_advantage, hero_win_rate, hero_number_of_matches):
            best_versus_hero[hn] = Info(ha, hwr, hnom)

        hero['best_versus'] = best_versus_hero
        hero['name'] = selector.xpath('//*[@id="content-header-primary"]/div[2]/h1/text()').extract()[0]

        return hero
