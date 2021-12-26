# -!- coding: utf-8 -!-
import pymysql
from pyecharts.charts import Map
from pyecharts import options as opts

city_list=['广州市','深圳市','清远市','佛山市','汕头市',
           '汕尾市','肇庆市','珠海市','湛江市','东莞市',
           '韶关市','河源市','梅州市','惠州市','潮州市',
           '揭阳市','中山市','江门市','阳江市','茂名市','云浮市']

def query():
    conn = pymysql.connect(host='127.0.0.1', port=3306, db='jianzhimao', user='root', password='')
    cursor = conn.cursor()
    count_list = []
    for city in city_list:
        city = city.split('市')[0]
        sql=f'''
            SELECT COUNT(details.id) FROM jianzhimao.details,jianzhimao.area where area.area_name=details.area_name and area.city_name='{city}'; 
        '''
        cursor.execute(sql)
        count = cursor.fetchall()[0][0]
        count_list.append(count)
    print(count_list)
    return count_list
def showData():
    count_list=query()
    map = Map()
    map.add('',[list(c) for c in zip(city_list,count_list)],'广东')
    map.set_global_opts(title_opts=opts.TitleOpts(title='广东兼职猫数据'),visualmap_opts=opts.VisualMapOpts(max_=3000))
    return map

if __name__=='__main__':
    c=showData()
    c.render('./jzm_guangdong.html')
