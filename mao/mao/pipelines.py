# -!- coding: utf-8 -!-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import pymysql
import json
import csv
from mao.items import CityItem,AreaItem,TitleItem
import mao.Createtable
import mao.Sha1Util


# 定义mysql数据库的管道类，把item存进数据库
class MYSQLPipeline(object):
    # open_spider()方法是在Spider开启的时候被自动调用的,仅被调用一次
    def open_spider(self, spider):
        # 调用Createtable的createtable()方法，创建city，area，details表
        mao.Createtable.createtable()
        # 创建mysql数据库连接
        self.db_coon = pymysql.connect(host='127.0.0.1', port=3306, db='text', user='root', password='', charset='utf8')
        # 获取获取游标对象
        self.db_cur = self.db_coon.cursor()

    # process_item()方法接受item和spider，其中spider表示当前传递item过来的spider
    def process_item(self, item, spider):
        # 使用isinstanc函数区分爬虫类，这里是CityItem类
        if isinstance(item,CityItem):
            # 调用Sha1Util中的jia_mi（）方法，对item['city_href']和item['city_name']进行加密，目地是得到长度为40独一无二的字符串，方便去重
            id = mao.Sha1Util.jia_mi(item['city_href']+item['city_name'])
            values=(id,item['city_href'],item['city_name'])
            try:
                    # 向city表中插入id,city_href,city_name的值，用主键primary或者唯一索引unique区分了记录的唯一性，
                    # ignore会忽略数据库中已经存在的数据，如果数据库没有数据，就插入新的数据，如果有数据的话就跳过这条数据
                    sql = '''insert ignore into text.city(id,city_href,city_name) values(%s,%s,%s);'''
                    # 执行sql语句
                    self.db_cur.execute(sql,values)
                    # 提交事务
                    self.db_coon.commit()
                    # print(f'{values}插入成功')
            except Exception as e:
                print(e)
                print(f'{values}插入失败')
                # 数据回滚
                self.db_conn.rollback()
        # 这里是AreaItem类
        elif isinstance(item, AreaItem):
            id = mao.Sha1Util.jia_mi(item['area_name'] + item['area_href'])
            values=(id,item['city_name'],item['area_name'],item['area_href'])
            try:
                    # 向area表中插入id,city_name,area_name,area_href的值
                    sql = "insert ignore into text.area(id,city_name,area_name,area_href) values(%s,%s,%s,%s);"
                    self.db_cur.execute(sql, values)
                    # print(f'{values}插入成功')
            except Exception as e:
                    print(e)
                    print(f'{values}插入失败')
                    self.db_coon.rollback()

        elif isinstance(item,TitleItem):

            id = mao.Sha1Util.jia_mi(item['area_name'] + item['title_href'])
            values=(id,item['area_name'],item['title_href'],item['job_title'],
                    item['views'],item['publish_time'],item['position_type'],
                    item['recruiting_numbers'],item['job_area'],item['job_type'],
                    item['time_request'],item['weekly_least'], item['job_hours'],
                    item['salary_type'],item['base_salary'],item['job_details'],
                    item['company'],item['company_brief'],item['company_address']
                    )

            try:
                    # 向details表中插入id, area_name等一系列字段的值
                    sql = "insert ignore into text.details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

                    self.db_cur.execute(sql, values)
                    self.db_coon.commit()
                    print(f'{values}插入成功')
            except Exception as e:
                print(e)
                print(f'{values}插入失败')
                self.db_coon.rollback()
        return item

    # close_spider()方法是在Spider关闭的时候被自动调用的,仅被调用一次
    def close_spider(self,spider):
        # 关闭游标对象
        self.db_cur.close()
        # 关闭mysql数据库连接
        self.db_coon.close()
        print('数据库关闭成功')


# 定义Json管道类，把item存储为json文件。
class JsonPipeline(object):
    def __init__(self):
        self.city_file = open('city.json', 'w',encoding='utf-8',errors='ignore')
        self.area_file = open('area.json', 'w',encoding='utf-8',errors='ignore')
        self.details_file = open('details.json', 'w',encoding='utf-8',errors='ignore')

    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            conent = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.city_file.write(conent)

        elif isinstance(item, AreaItem):
            conent = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.area_file.write(conent)

        elif isinstance(item, TitleItem):
            conent = json.dumps(dict(item), ensure_ascii=False)+ ",\n"
            self.details_file.write(conent)
        return item

    def close_spider(self, spider):
        self.city_file.close()
        self.area_file.close()
        self.details_file.close()


# 定义csv管道类，把item存储为csv文件
class CSVPipeline(object):
    def __init__(self):
        self.city_file = open('city.csv', 'w',newline="",encoding='utf-8',errors='ignore')
        self.area_file = open('area.csv', 'w', newline="",encoding='utf-8',errors='ignore')
        self.details_file = open('details.csv', 'w', newline="",encoding='utf-8',errors='ignore')

        self.city_field = ['city_href', 'city_name']
        self.city_writer = csv.DictWriter(self.city_file, fieldnames=self.city_field )

        self.area_field = ['city_name', 'area_name', 'area_href']
        self.area_writer = csv.DictWriter(self.area_file, fieldnames=self.area_field)

        self.details_field = ['area_name', 'title_href', 'job_title', 'views', 'publish_time', 'position_name',
                           'recruiting_numbers', 'job_area', 'job_type', 'job_time', 'job_hours', 'salary_type',
                           'base_salary', 'job_details', 'company', 'company_brief', 'company_address']
        self.details_writer = csv.DictWriter(self.details_file, fieldnames=self.details_field )

        self.city_writer.writeheader()
        self.area_writer.writeheader()
        self.details_writer.writeheader()


    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            self.city_writer.writerow(item)

        elif isinstance(item, AreaItem):
            self.area_writer.writerow(item)

        elif isinstance(item, TitleItem):
            self.details_writer.writerow(item)

        return item

    def close_spider(self, spider):
        self.city_file.close()
        self.area_file.close()
        self.details_file.close()
        self.index_file.close()