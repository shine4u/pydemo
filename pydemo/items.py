# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AvfanhaoItem(scrapy.Item):
    cn_name = scrapy.Field() #  Chinese name.
    jp_name = scrapy.Field() #  Japanese name.
    en_name = scrapy.Field() # English name.
    infos = scrapy.Field() # list of key value. 生日，星座，血型
    prods = scrapy.Field() # list of products, each one is pair (fanhao prodname videolen publishtime publisher)
    intro = scrapy.Field() # the introduction of Av star.
