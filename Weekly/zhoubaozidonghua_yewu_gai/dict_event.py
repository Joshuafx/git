#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename:dict_event.py

#从analysis，details，historical_tracing返回数据到字典
import MySQLdb
from B_Suspicious_point import *
conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
cur=conn.cursor()
#python无法直接修改tuple，使用list保存value
def dict_ev(dic,table,key):
    cur.execute('select * from '+table)
    select=cur.fetchall()
    for n in range(0,len(select)):
        k=key+str(n+1)
        dic[k]=list(select[n])

dict_h={}
dict_ev(dict_h,'historical_tracing','h')
dict_d={}
dict_ev(dict_d,'details','d')
dict_a={}
dict_ev(dict_a,'analysis','a')
