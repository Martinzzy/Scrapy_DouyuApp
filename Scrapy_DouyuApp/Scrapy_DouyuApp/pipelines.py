# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class ScrapyDouyuappPipeline(object):
    def process_item(self, item, spider):
        return item


#twisted只是提供一个容器，进行异步存储
class MySQLTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWORD'],
                port = settings['MYSQL_PORT'],
                charset = 'utf8',
                cursorclass = pymysql.cursors.DictCursor,
                use_unicode = True,
            )

        dbpool = adbapi.ConnectionPool("pymysql",**dbparms)
        return cls(dbpool)


    def process_item(self,item,spider):
        #使用twisted使mysql的插入编程异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider) #处理异常


    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):

        #根据不同item，构建不同的sql语句并插入到mysql中
        #执行具体的插入
        #这样可以在具体的items中处理具体的信息，然后写insert_sql语句

        insert_sql,params = item.get_insert_sql()

        cursor.execute(insert_sql,params)


from scrapy.pipelines.images import ImagesPipeline
from settings import IMAGES_STORE
import os

class DouyuImagePipeline(ImagesPipeline):


    def item_completed(self, result, item, info):

        image_path = [x["path"] for ok, x in result if ok]

        os.rename(IMAGES_STORE + "/" + image_path[0], IMAGES_STORE + "/" + item["nickname"] + ".jpg")

        item["image_path"] = IMAGES_STORE + "/" + item["nickname"]

        return item


