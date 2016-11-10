from scrapy.item import Item, Field

class TelegraphItem(Item):
    title = Field()
    link = Field()
    article = Field()
    date = Field()
