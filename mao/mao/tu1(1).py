import pymysql
# import pyecharts.charts
# from pyecharts import Bar
from pyecharts.charts import Bar
from pyecharts import options as opts
city_list = ['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆', '武汉', '西安', '苏州', '天津', '南京', '长沙', '郑州', '东莞', '青岛', '沈阳', '宁波', '无锡']
def p():
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', database='jianzhimao', charset='utf8')
    # 获取游标对象
    cursor = conn.cursor()
    count_list = []
    for city in city_list:
        sql = '''select COUNT(d.id) from  area a  ,details d where a.city_name = \'{}\' and a.area_name = d.area_name'''.format(city)
        print(sql)
        cursor.execute(sql)
        count = cursor.fetchall()[0][0]
        # print(count)
        count_list.append(count)
    return count_list
def bar_picture():
    count_list = p()
    #获取柱状图对象
    bar = Bar()
    # 填充数据
    bar.add_xaxis(city_list) #
    bar.add_yaxis('岗位数量',count_list)
    # 添加选项
    bar.title='一线城市兼职岗位数量' #添加标题
    bar.set_series_opts(label_opts=opts.LabelOpts(position='top'))
    bar.render('./jzm_bar.html')
if __name__ == '__main__':
    bar_picture()