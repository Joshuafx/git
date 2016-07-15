#!/usr/bin/python

import zhoubaozidonghua_shijian
import zhoubaozidonghua_yewu_gai.B_calculate_Y

import MySQLdb
# conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
conn = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='123456', db='event_history', port=3306)
cur = conn.cursor()

cur.execute('select business,eventname,m_name_key,ipaddress,happentime,maintainlevel,ui_event_av,event_num from business_analysis WHERE period='+\
         zhoubaozidonghua_yewu_gai.B_calculate_Y.list_period_set[-1])

