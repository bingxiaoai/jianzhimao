# -!- coding: utf-8 -!-
import scrapy
from mao.items import CityItem,AreaItem,TitleItem
import re

from scrapy_redis.spiders import RedisSpider
# class MaoSpider(RedisSpider):

class MaoSpider(scrapy.Spider):
    # 爬虫名称
    name = 'xiaomao'

    # allowed_domains为允许的域
    allowed_domains = ['https://www.jianzhimao.com']

    # start_urls为爬虫开始的请求列表
    start_urls = ['https://www.jianzhimao.com/ctrlcity/changeCity.html']
#     redis_key = 'py'
#
#     def __init__(self,*args,**kwargs):
#         domain=kwargs.pop('domain','')
#         self.allowed_domains = list(filter(None,domain.split(',')))
#         super(MaoSpider,self).__init__(*args,**kwargs)


    # 爬取城市页面‘https://www.jianzhimao.com/ctrlcity/changeCity.html’的全部城市及其链接
    # parse(self, response): 当请求url返回网页没有指定回调函数，默认的Request对象的回调函数，用来处理网页返回的response，和生成的Item或者Request对象
    def parse(self, response):
        node_list = response.xpath("//ul[@class='city_table']/li/a")
        for node in node_list:
            item = CityItem()  # 创建CityItem对象
            item['city_href'] = node.xpath("./@href").get()   # 获取城市名字
            item['city_name'] = node.xpath("./text()").get()  # 获取城市链接

            # 把http替换成https，用于下面scrapy.Request识别并发起请求
            item['city_href'] = item['city_href'].replace('http', 'https')
            # 把item值返回到pipeline管道文件中
            yield item
            # 构造Request对象，把item['city_href']请求交给引擎；callback指定解析函数名称，表示该请求返回的响应使用area_parse函数进行解析
            yield scrapy.Request(item['city_href'],callback=self.area_parse)

    # 爬取每个城市页面的区域名称以及链接，例如广州‘https://guangzhou.jianzhimao.com/’
    def area_parse(self, response):
        # response.request.url:当前响应对应的请求的url地址,findall匹配从h开始到com结束的任意内容返回到列表中，并取出下标为0的值
        # 例如获取响应请求为https://guangzhou.jianzhimao.com/，得到的city_url为https://guangzhou.jianzhimao.com
        city_url=re.findall(r'h.*com', response.request.url)[0]

        # 这里做个判断，判断响应状态码是否为500，如果是，就无法获取信息，例如：https://wuzhishan.jianzhimao.com/
        if response.status == 500:
            print(response.url)
        else:
            area_list = response.xpath("//body/section[1]/article/aside/div[2]/ul/li[3]/a")
            for key in area_list:
                area_name = key.xpath("./text()").get()  # 获取区域名称
                if area_name == '不限': # 区域名称里有‘不限’，我们不需要它
                    pass
                else:
                    city_name = response.xpath("//body/header/nav/div[1]/span/text()").get()  # 这里获取到城市名称是本页面的城市名称
                    area_href = key.xpath("./@href").get()  # 获取区域链接

                    item = AreaItem()  # 创建AreaItem对象
                    item['city_name'] = city_name
                    item['area_name'] = area_name
                    item['area_href'] = area_href

                    # 将city_url与区域链接拼接得到完整的区域链接,
                    # 例如https://guangzhou.jianzhimao.com + /tianhe_zbx_0/ --> https://guangzhou.jianzhimao.com/tianhe_zbx_0/
                    item['area_href'] = city_url + item['area_href']
                    # item['area_href'] = response.urljoin(item['area_href'])
                    # print(item['area_href'])

                    yield item  # 把item值返回到pipeline管道文件中
                    # 构造Request对象，把item['area_href']请求交给引擎；callback指定解析函数名称，表示该请求返回的响应使用title_parse函数进行解析
                    yield scrapy.Request(item['area_href'], callback=self.title_parse)


    # 爬取爬取每个城市页面里每个区域的标题信息（区域名称，标题，浏览量，发布时间，标题链接）
    def title_parse(self, response):
        # response.request.url:当前响应对应的请求的url地址,findall匹配从h开始到com结束的任意内容返回到列表中，并取出下标为0的值
        # 例如获取响应请求为https://guangzhou.jianzhimao.com/tianhe_zbx_0/，得到的city_url为https://guangzhou.jianzhimao.com
        # city_url = re.findall(r'h.*com', response.request.url)[0]

        kong=response.xpath("/html/body/section[1]/article/div[2]/div[1]/ul/li/div/div/text()").get()
        if kong == '抱歉，没找到你要的信息' or response.status == 500:  # 有些页面没有招聘信息或者响应状态码为500
            pass
        else:
            title_list = response.xpath("//ul[@class='content_list_wrap']/li")
            for key in title_list:
                    area_name = key.xpath("./div[@class='left area']/span/text()").get()  # 这里的区域名称也与上面的区域名称不同，是独立获取的
                    job_title = key.xpath("./a/text()").get()  # 获取标题
                    views = key.xpath("./div[@class='left visited']/span/text()").get()  # 获取浏览量
                    publish_time = key.xpath("./div[@class='left date']/text()[2]").get()  # 获取发布时间
                    title_href = key.xpath("./a/@href").get()  # 获取标题链接

                    item = TitleItem()  # 创建TitleItem对象

                    # strip()表示去掉首尾的空格
                    item['area_name'] = area_name.strip()
                    item['job_title'] = job_title.strip()
                    item['views'] = views.strip()
                    item['publish_time'] = publish_time.strip()

                    item['title_href'] = title_href
                    # 将city_url与标题链接拼接得到完整的标题链接,
                    # 例如https://guangzhou.jianzhimao.com/ + /job/YTBJa3dWU3FvbDg9.html --> https://guangzhou.jianzhimao.com/job/YTBJa3dWU3FvbDg9.html
                    # item['title_href'] = str(city_url) + item['title_href']
                    item['title_href'] = response.urljoin(item['title_href'])
                    print( item['title_href'])

                    # 构造Request对象，把item['title_href']请求交给引擎；callback指定解析函数名称，表示该请求返回的响应使用details_parse函数进行解析
                    # meta实现数据在不同的解析函数中的传递，meta将上面的item值传递到details_parse函数中
                    yield scrapy.Request(item['title_href'],callback=self.details_parse,meta={'item': item})

            next_url = response.xpath("//li[@class='next']/a/@href").get()  # 获取下一页
            if next_url is not None:
                    # 将city_url与 下一页next_url拼接，例如 https://guangzhou.jianzhimao.com + /tianhe_zbx_0/index8.html --> https://guangzhou.jianzhimao.com/tianhe_zbx_0/index8.html
                    # next_url = str(city_url) + next_url
                    next_url = response.urljoin(next_url)
                    # print(next_url)
                    # 构造Request对象，把next_url请求交给引擎；callback指定解析函数名称，表示该请求返回的响应使用title_parse函数进行解析
                    yield scrapy.Request(next_url,callback=self.title_parse)


# 爬取详情页面的信息
    def details_parse(self, response):
        list = response.xpath("/html/body/section/article/div/div[1]")
        for each in list:
            # 获取由meta传递的item字段（区域名称，标题，浏览量，发布时间，标题链接）
            item = response.meta['item']
            # 获取职位类别
            position_type = each.xpath("./div[2]/div[1]/div[1]/a/text()").get()
            # 获取招聘人数
            recruiting_numbers = each.xpath("./div[2]/div[2]/ul[1]/li[1]/span[2]/text()").get()
            # 获取工作地点
            job_area = each.xpath("./div[2]/div[2]/ul[1]/li[2]/span[2]/text()").get()
            # 获取工作详情
            job_details = each.xpath("./div[2]/div[2]/div[@class='box']/div[2]/text()").extract()
            # 获取公司名称
            company = each.xpath("./div[3]/div[2]/div[1]/div[2]/a/text()").get()
            # 获取公司介绍
            company_brief = each.xpath("./div[3]/div[2]/div[1]/div[2]/p[1]/text()").extract()
            # 获取公司地址
            company_address = each.xpath("./div[3]/div[2]/div[1]/div[2]/p[2]/text()").get()

            # 工作类别不同，字段的位置会不同
            if len(each.xpath("./div[2]/div[2]/ul[2]/li")) ==3:
                # 短招
                # 获取工作类别，这里为短招
                job_type = each.xpath("./div[2]/div[2]/ul[2]/li[1]/span[2]/text()").get()
                # 这里为短招，字段为工作时间
                time_request = each.xpath("./div[2]/div[2]/ul[2]/li[2]/span[2]/text()").get()
                # 获取上班时段
                job_hours = each.xpath("./div[2]/div[2]/ul[2]/li[3]/span[2]/text()").extract()
                item['weekly_least'] = 'null'  # 这里为短招，没有该字段，设置为空
            else:
                # 长招
                # 这里为长招，字段为时间要求
                time_request = each.xpath("./div[2]/div[2]/ul[2]/li[1]/span[2]/text()").get()
                # 获取工作类别，这里为长招
                job_type = each.xpath("./div[2]/div[2]/ul[2]/li[2]/span[2]/text()").get()
                # 获取字段为每周至少的内容
                weekly_least = each.xpath("./div[2]/div[2]/ul[2]/li[3]/span[2]/text()").get()
                item['weekly_least'] = weekly_least
                # 获取上班时段
                job_hours= each.xpath("./div[2]/div[2]/ul[2]/li[4]/span[2]/text()").extract()
            # 获取结算方式
            salary_type = each.xpath("./div[2]/div[2]/ul[3]/li[1]/span[2]/text()").get()
            # 获取基本工资
            base_salary = each.xpath("./div[2]/div[2]/ul[3]/li[2]/span[2]/text()").get()
            item['position_type'] = position_type
            item['recruiting_numbers'] = recruiting_numbers
            item['job_area'] = job_area
            item['job_type'] = job_type.strip()
            item['job_hours'] = job_hours

            item['job_hours'] = ','.join(item['job_hours'])
            item['job_hours'] = item['job_hours'].split()
            item['job_hours'] = ','.join(item['job_hours'])

            item['time_request'] = time_request
            item['salary_type'] = salary_type.strip()
            item['base_salary'] = base_salary.strip()

            item['job_details'] = job_details
            item['job_details'] = ' '.join(item['job_details'])
            item['job_details'] = item['job_details'].split()
            item['job_details'] = ' '.join(item['job_details'])

            item['company'] = company.strip()
            if len(company_brief) == 0:
                item['company_brief']='null'
            else:
                item['company_brief'] = company_brief
                item['company_brief'] = ','.join(item['company_brief'])
                item['company_brief'] = re.sub('[\s+]','',item['company_brief'])

            item['company_address'] = company_address.strip()

            yield item



