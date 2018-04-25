# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from settings import SQL_DATETIME_FORMAT

class ScrapyDouyuappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DouyuItem(scrapy.Item):

    room_id = scrapy.Field()
    room_name = scrapy.Field()
    images_url = scrapy.Field()
    image_path = scrapy.Field()
    nickname = scrapy.Field()
    city = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
            insert into yanzhi(id,name,nickname,city,crawl_time) VALUES (%s,%s,%s,%s,%s)
        """
        params = (self["room_id"],self["room_name"],self["nickname"],self["city"],self["crawl_time"].strftime(SQL_DATETIME_FORMAT))

        return insert_sql,params