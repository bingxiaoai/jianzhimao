# -!- coding: utf-8 -!-
import pymysql
from pyecharts.charts import Map
from pyecharts import options as opts

conn = pymysql.connect(host='127.0.0.1', port=3306, db='jianzhimao', user='root', password='')

def quanguo():
    city_list=[]
    cursor = conn.cursor()
    sql = '''
        select city_name from jianzhimao.city;
    '''
    cursor.execute(sql)
    count = cursor.fetchall()
    for city in count:
        # print(city)
        city_list.append(city[0])
    return city_list

# city_list=quanguo()
# print(city_list)

def query():
    city_list=quanguo()
    count_list = []
    cursor = conn.cursor()
    for city in city_list:
        # city = city.split('市')[0]
        sql=f'''
            SELECT COUNT(details.id) FROM jianzhimao.details,jianzhimao.area where area.area_name=details.area_name and area.city_name='{city}';
        '''
        cursor.execute(sql)
        count=cursor.fetchall()[0][0]
        count_list.append(count)
        # print(count_list)
    return count_list
def showData():
    count_list=query()
    city_list=quanguo()
    map = Map()
    map.add('',[list(c) for c in zip(city_list,count_list)],'china')
    map.set_global_opts(title_opts=opts.TitleOpts(title='中国兼职猫数据'),visualmap_opts=opts.VisualMapOpts(max_=3000))
    return map

if __name__=='__main__':
    c=showData()
    c.render('./jzm_quanguo.html')