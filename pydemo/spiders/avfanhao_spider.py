#coding=utf-8

import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import re, logging, json

from pydemo.items import AvfanhaoItem

MIN_PAGE_ID = 148
MAX_PAGE_ID = 151

LIST_URL_PAT = r'http://avfanhao.net/page/(\d+)/'
LIST_URL_HOME = 'http://avfanhao.net/'

def process_list_url(url):
    pageid = 0
    if url == LIST_URL_HOME: pageid = 1
    else:
        mo = re.match(LIST_URL_PAT, url)
        if not mo: return None
        pageid = int(mo.group(1))
   
    if pageid < MIN_PAGE_ID or pageid >= MAX_PAGE_ID: return None
    return url

class AvfanhaoSpider(CrawlSpider):
    name = 'avfanhao'
    allowed_domains = ['avfanhao.net',] # 允许的来源
    start_urls = ['http://avfanhao.net/page/149/'] # 入口页面
       
    rules = (
             # 翻页
             Rule(LinkExtractor(allow=(LIST_URL_PAT, LIST_URL_HOME), restrict_xpaths='//nav[@class="pagination loop-pagination"]', process_value=process_list_url)),
            
             # list -> cont
             # parse_cont不存在link关系，所有返回都为item.
             Rule(LinkExtractor(allow=(LIST_URL_PAT, LIST_URL_HOME), restrict_xpaths='//h2[@class="entry-title"]'), callback='parse_cont'),
             )
   
    def __init__(self, *a, **kw):
        super(AvfanhaoSpider, self).__init__(*a, **kw)

    # 处理详情页, 二级页面, 分番号数据 & 女优信息数据
    def parse_cont(self, response):
        selector = Selector(response=response)

        # 标题信息
        cont_title = selector.xpath('//h1[@class="entry-title"]/a/text()').extract_first().replace('\n','').strip()
       
        # 文章分类信息 如果是AV女优 则记录数据
        cate_name = selector.xpath('//div[@class="entry-meta"]/span/a/text()').extract_first().replace('\n','').strip()
        if cate_name.encode('utf8') != "AV女优": return 
       
        # 作品列表
        prods = []
        fanhaos = selector.xpath('//table[@class="fanhao_list_table"]/tbody/tr')
        for fid, item in enumerate(fanhaos):
            itemdetail = item.xpath('.//td').extract() # td.text() is wrong.
            if len(itemdetail) != 5: # fanhao, videoname, videolen, publishtime, publisher
                logging.warn('itemdetail len error itemdetail=[%s], discard it.' % itemdetail)
                continue
            prods.append(itemdetail)
           
        # 女优简介
        intro = selector.xpath('//div[@class="entry-content"]/p').extract_first().replace('\n','').strip()
       
        # 女优信息
        jp_name, cn_name, en_name = '', '', ''
        infos = []
        items = selector.xpath('//div[@class="entry-content"]/p/text()').extract()
        for item in items:
            tokens = item.encode('utf8').replace('\n','').replace('：', ':').strip().split(':')
            # logging.debug(tokens)
            if len(tokens) != 2: continue
            if  tokens[0] == '中文名' or tokens[0] == '中文': cn_name = tokens[1]
            elif tokens[0] == '日文名' or tokens[0] == '日文': jp_name = tokens[1]
            elif tokens[0] == '英文名' or tokens[0] == '英文': en_name = tokens[1]
            elif tokens[0] == '姓名': jp_name = tokens[1]
            else: infos.append(tokens)
        yield AvfanhaoItem(cn_name=cn_name, jp_name=jp_name, en_name=en_name, infos=infos,
                           prods=prods, intro=intro, item_url=response.url)
