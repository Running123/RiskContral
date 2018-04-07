#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-05-05 05:59:23
# Project: phone_price

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://list.suning.com/0-20006-0.html',fetch_type='js',callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://product.suning.com"]').items():
            if re.match('http://product.suning.com/.*.html$',each.attr.href):  
                self.crawl(each.attr.href,fetch_type='js',callback=self.detail_page)
        self.crawl("http://list.suning.com%s"%response.doc('.second-filter .r-btn').attr.href,fetch_type='js', callback=self.index_page)

    @config(priority=3)
    def detail_page(self, response): 
        return {
            "url":response.url,
            "title":response.doc('title').text(),
            "gds_cd":response.doc('#partNumberLable').text(),
            "price":response.doc('.mainprice').text(),
            "vendor_tp":response.doc('input#vendorType').attr.value
        }
