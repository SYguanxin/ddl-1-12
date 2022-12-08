# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from bilibili.items import BilibiliItem, AssessItem

class BilibiliPipeline:
    db = None
    cursor = None
    def open_spider(self,spider):
        self.db = pymysql.connect(host='localhost',
                             user='root',
                             password='csm.zhinai.123',
                             database='bilibili')
        self.cursor = self.db.cursor()
        self.cursor.execute('drop table if exists QWE_as')
        sql = """create table QWE_as (
                             like_num INT,
                             Toubi INT,
                             Shoucang INT,
                             assess INT )"""
        self.cursor.execute(sql)
        self.cursor.execute('drop table if exists Assess')
        sql = """create table Assess (
                             name char(30),
                             content TEXT,
                             assess_time char(21),
                             assess_like INT,
                             _sub boolean)"""
        self.cursor.execute(sql)
    def process_item(self, item, spider):
        if isinstance(item, BilibiliItem):
            try:
                self.cursor.execute('insert into QWE_as values(%d,%d,%d,%d)'
                                %(item['QWE_as']['点赞（Q）'],item['QWE_as']['投币（W）'],item['QWE_as']['收藏（E）'],item['QWE_as']['评论（A）']))
                self.db.commit()
            except:
                self.db.rollback()
            print(item['QWE_as'])
        elif isinstance(item, AssessItem):
            try:
                self.cursor.execute('insert into Assess values("%s","%s","%s",%s,%s)'
                                % (item['name'],item['content'],item['assess_time'],item['like'],item['sub']))
                self.db.commit()
            except:
                self.db.rollback()
        return item
    def close_spider(self,spider):
        self.db.close()
