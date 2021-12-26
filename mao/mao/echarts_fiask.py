from flask import Flask, render_template
import pymysql
#开头
app = Flask(__name__)
    #连接数据库
conn = pymysql.connect(host='127.0.0.1', port=3306, db='jianzhimao', user='root', password='')
cursor = conn.cursor() #游标的创建
#数据库查询
sql ='''
SELECT position_type,sum(views)  from jianzhimao.details GROUP BY position_type HAVING COUNT(position_type)>10 ;
        '''
#执行查询的数据游标
cursor.execute(sql)
item=cursor.fetchall()
# type_list=[]
# views_list=[]
# for type in count:
#     # print(city)
#     type_list.append(type[0])
#     views_list.append(type[1])

# print(type_list)
# print(views_list)
cursor.close()
conn.close()

#路由
@app.route("/")
def mysql():
    return render_template('echarts.html',items=item) #返回函数并引用HTML模板
#项目名main
if __name__ == '__main__':
    app.run(debug=True) #执行并开启debug模式