#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-05-05 05:59:23
# Project: brand

from pyspider.libs.base_handler import *
import re
import json

class Handler(BaseHandler):
    crawl_config = {
         'headers': {
            'User-Agent': 'GoogleBot',
            }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://list.suning.com/0-157162-0.html', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://product.suning.com"]').items():
            if re.match('http://product.suning.com/.*.html$',each.attr.href):  
                self.crawl(each.attr.href,callback=self.detail_page)
        self.crawl([x.attr.href for x in response.doc('div#bottom_pager > a[name^="ssdln_157162_bottom_page-"] ').items()], callback=self.index_page)

    @config(priority=1)
    def detail_page(self, response):    
        price_url = "http://icps.suning.com/icps-web/getAllPriceFourPage/000000000%s_0000000000_025_0250101_1_pc_showSaleStatus.vhtm"%(response.doc('#partNumberLable').text())
        self.crawl(price_url, callback=self.price_page)
        
    @config(priority=2)
    def price_page(self, response):
       data = re.compile(u'"partNumber":"000000000(.*)","refPrice":"(.*)","netPrice":"(.*)","promotionPrice":"(.*)","priceType"')
       result = re.search(data, response.text)
     
       return  {
                "url":'http://product.suning.com/%s.html'%result.group(1),
                "gds_cd": result.group(1),
                "refPrice": result.group(2),
                "netPrice": result.group(3),
                "promotionPrice":result.group(4),
             }
