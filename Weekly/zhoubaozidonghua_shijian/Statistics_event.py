#!/usr/bin/env python 
#-*- coding:utf-8 -*-

a='' b='' c=''

import MySQLdb
conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',\
                     db='test',port=3306)#charset='utf8'
cur=conn.cursor()

cur.execute("load data local infile 'D:/Tool/Python27/work/zhoubaozidonghua/open_event_data.txt' into table open_event_data")

