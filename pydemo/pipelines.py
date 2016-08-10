# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pydemo.items import AvfanhaoItem

class PydemoPipeline(object):
    def process_item(self, item, spider):
        field_empty_cnt = 0
        if item['cn_name'] == '': field_empty_cnt += 1
        if item['en_name'] == '': field_empty_cnt += 1
        if item['jp_name'] == '': field_empty_cnt += 1
        if len(item['infos']) == 0: field_empty_cnt += 1
        if len(item['prods']) == 0: field_empty_cnt += 1
        if field_empty_cnt <= 3:
            logging.warn('too many field_empty_cnt=[%d] item=%s' % (field_empty_cnt, item)) 

        return item
