# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    QWE_as = scrapy.Field()
class AssessItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    assess_time = scrapy.Field()
    like = scrapy.Field()
    sub = scrapy.Field()
