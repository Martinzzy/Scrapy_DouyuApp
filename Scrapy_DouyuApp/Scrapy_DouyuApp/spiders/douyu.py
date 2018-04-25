# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from ..items import DouyuItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn/api/v1/getVerticalRoom']
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset={0}'
    offset = 0
    start_urls = [base_url.format(offset)]

    def parse(self, response):

        #解析json数据
        data = json.loads(response.text)["data"]
        for each in data:
            zhibo = DouyuItem()
            room_id = each["room_id"]
            id = int(room_id)
            room_name = each["room_name"]
            nickname = each["nickname"]
            image_url = each["vertical_src"]
            city = each["anchor_city"]


            zhibo["room_id"] = id
            zhibo["room_name"] = room_name
            zhibo["images_url"] = [image_url]
            zhibo["nickname"] = nickname
            zhibo["city"] = city
            zhibo["crawl_time"] = datetime.datetime.now()

            yield zhibo

        #构建下一页的Request对象
        self.offset +=20
        yield scrapy.Request(url=self.base_url.format(self.offset),callback=self.parse,dont_filter=True)