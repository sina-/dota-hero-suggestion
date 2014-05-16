from scrapy.item import Item, Field


class HeroItem(Item):
    url = Field()
    name = Field()
