#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filname:calculate_Y.py

#周期数Ncycle 目前先手动输入
#当期事件总数量Nevent_sum
#√每个事件前N期报警数量Ui_event_av
#√当期每个事件报警数量Xi_event
#√每个事件的总历史数量SUMi_event
#√每个事件当期数量与前N期报警数量比值Yi_event=Xi_event/Ui_event_av

import MySQLdb
#conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
conn=MySQLdb.Connect(host='localhost',user='root',passwd='123456',db='event_history',port=3306)
cur=conn.cursor()

#得到目前所有的period
cur.execute('select period from open_event_data')
all_period=cur.fetchall()
list_period=[]
for n in all_period:
    list_period.append(n[0])
list_period_set=list(set(list_period))
list_period_set.sort()
len_period=len(list_period_set)

#得到目前所有的eventname
cur.execute('select eventname from open_event_data')
all_eventname=cur.fetchall()
list_eventname=[]
for n in all_eventname:
    list_eventname.append(n[0])
list_eventname_set=list(set(list_eventname))

#计算Xi_event
Xi_event=[]
for n in list_eventname_set:
    SQL='select ifnull(count(eventname),0) from open_event_data where eventname=\"'+n+'\"'+' and period='+list_period_set[-1]
    cur.execute(SQL)
    Xi_event.append(cur.fetchall()[0][0])
print Xi_event

#计算Ui_event_av
#Ncycle=input('请输入周期数：')
Ui_event=[]
Ui_event_av=[]
len_eventname=len(list_eventname_set)
for n,m in zip(list_eventname_set,range(0,len_eventname)):
    SQL='select ifnull(count(eventname),0) from open_event_data where eventname=\"'+n+'\"'+' and period between '+list_period_set[0]+\
    ' and '+list_period_set[-2]
    cur.execute(SQL)
    Ui_event.append(cur.fetchall()[0][0])
    Ui_event_av.append((float(Ui_event[m])/len_period))

#计算SUMi_event
SUMi_event=[]
for n in list_eventname_set:
    SQL='select ifnull(count(eventname),0) from open_event_data where eventname=\"'+n+'\"'
    cur.execute(SQL)
    SUMi_event.append(cur.fetchall()[0][0])

#根据Xi_event是否大于1，用不同的公式计算Y
def compare_1(arg1,n):
    if arg1>=1:
        return Xi_event[n]/Ui_event_av[n]
    elif arg1<1:
        return Xi_event[n]/SUMi_event[n]
        
#求Yi_event
Yi_event=[]
for n in range(0,len_eventname):
    Yi_event.append(compare_1(Ui_event_av[n],n))
print Yi_event
