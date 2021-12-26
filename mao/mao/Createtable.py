# -!- coding: utf-8 -!-
import pymysql
def createtable():
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', database='jianzhimao', charset='utf8')
    # 获取游标对象
    cursor = conn.cursor()
    conn.begin()
    try:
        sql = """
        CREATE TABLE if not exists `city` (
        `id` varchar(50) NOT NULL,
        `city_href` varchar(100) default NULL,
        `city_name` varchar(100) default NULL,
        `status` int(1) default '0' COMMENT '状态',
        PRIMARY KEY  (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
        """
        cursor.execute(sql)
        print('city表创建成功')
    except Exception as e:
        print(e)
    try:
        sql = """
        CREATE TABLE if not exists `area` (
        `id`  varchar(50) NOT NULL,
        `city_name` varchar(100) default NULL COMMENT '区县',
        `area_name` varchar(100) default NULL COMMENT '所属城市',
        `area_href` longtext default NULL COMMENT '区县链接',
        `status` int(1) default '0' COMMENT '状态',
        PRIMARY KEY  (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8; 
        """
        cursor.execute(sql)
        print('area表创建成功')
    except Exception as e:
        print(e)
    try:
        sql = """
        CREATE TABLE if not exists `details` (
        `id`  varchar(50) NOT NULL,
        `area_name` varchar(100) default NULL COMMENT '所属城市',
        `title_href` varchar(100) default NULL COMMENT '标题信息链接',
        `job_title` varchar(100) default NULL COMMENT '标题',
        `views` varchar(100) default NULL COMMENT '浏览量',
        `publish_time` varchar(100) default NULL COMMENT '发布时间',
        `position_type` varchar(100) default NULL COMMENT '职位类别',
        `recruiting_numbers` varchar(100) default NULL COMMENT '招募人数',
        `job_area` varchar(100) default NULL COMMENT '工作地点',
        `job_type` varchar(100) default NULL COMMENT '工作类别',
        `time_request` varchar(100) default NULL COMMENT '在长招里叫时间要求,在短招里叫工作时间',
        `weekly_least` varchar(100) default NULL COMMENT '每周至少，这个是长招专属字段',
        `job_hours` varchar(100) default NULL COMMENT '上班时段',
        `salary_type` varchar(100) default NULL COMMENT '结算方式',
        `base_salary` varchar(100) default NULL COMMENT '基本工资',
        `job_details` text COMMENT '工作详情',
        `company` varchar(100) default NULL COMMENT '公司',
        `company_brief` varchar(1000) default NULL COMMENT '公司介绍',
        `company_address` varchar(150) default NULL COMMENT '公司地址',
        PRIMARY KEY  (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
        """
        cursor.execute(sql)
        print('details表创建成功')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()