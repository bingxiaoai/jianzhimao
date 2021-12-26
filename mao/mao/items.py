# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义爬虫类CityItem，并设置对应的item字段
class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_href = scrapy.Field()
    city_name = scrapy.Field()

# 定义爬虫类AreaItem，并设置对应的item字段
class AreaItem(scrapy.Item):

    city_name = scrapy.Field()
    area_name = scrapy.Field()
    area_href = scrapy.Field()

# 定义爬虫类TitleItem，并设置对应的item字段
class TitleItem(scrapy.Item):
    area_name = scrapy.Field()
    title_href = scrapy.Field()
    job_title = scrapy.Field()
    views = scrapy.Field()
    publish_time = scrapy.Field()

    position_type = scrapy.Field()
    recruiting_numbers = scrapy.Field()
    job_area = scrapy.Field()
    job_type = scrapy.Field()

    job_hours = scrapy.Field()
    time_request = scrapy.Field()
    weekly_least = scrapy.Field()
    salary_type = scrapy.Field()
    base_salary = scrapy.Field()
    job_details = scrapy.Field()

    company = scrapy.Field()
    company_brief = scrapy.Field()
    company_address = scrapy.Field()
# class IndexItem(scrapy.Item):
#     next_url = scrapy.Field()
