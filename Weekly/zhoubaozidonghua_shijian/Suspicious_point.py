#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename:Suspicious_point

#√置信水平Z，默认Z90
#√事件比值均值：Uevent-av
#√事件比值标准差：Sevent
#√区间估计上限：Pmax = Uevent-av + Z
#√区间估计下限：Pmin = Uevent-av - Z
#√Ievent高可疑异常点系数，可配置

#list_eventname_set:所有事件名称。Ui_event_av：每个事件前N期均值。Xi_event：当期每个事件报警数量。
#from calculate_Y import Yi_event,list_eventname_set,Ui_event_av,\
#     list_period_set,Xi_event
#import MySQLdb
from calculate_Y import *

#conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
#conn=MySQLdb.Connect(host='localhost',user='root',passwd='123456',db='event_history',port=3306)
#cur=conn.cursor()

Uevent_av=sum(Yi_event)/len(Yi_event)
SumY_sq=sum([(Yn-Uevent_av)**2 for Yn in Yi_event])
print SumY_sq
Sevent=(SumY_sq/len(Yi_event))**0.5
print Sevent

#正态分布表，置信水平为80%~99%
dict_Nd={80:1.28,81:1.31,82:1.34,83:1.37,84:1.41,\
         85:1.44,86:1.48,87:1.51,88:1.55,89:1.60,\
         90:1.64,91:1.69,92:1.75,93:1.81,94:1.88,\
         95:1.96,96:2.05,97:2.17,98:2.32,99:2.58}

#Z=dict_Nd[Z]*Uevent_av*Sevent
#Pmax = Uevent-av + Z
#Pmin = Uevent-av - Z
'''
list_Z=[]
Pmax=[]
Pmin=[]
for n in range(80,100):
    z=dict_Nd[n]*Uevent_av*Sevent
    list_Z.append(z)
    pmax=Uevent_av+z
    Pmax.append(pmax)
    pmin=Uevent_av-z
    Pmin.append(pmin)
'''

#可配置参数，置信水平暂时设为90%
Conf_lv=90
#Conf_lv=input('输入置信水平（80%~99%）：')
nd=dict_Nd[Conf_lv]
print nd
z=nd*Uevent_av*Sevent
print z
pmax=Uevent_av+z
print pmax
pmin=Uevent_av-z

#判断可疑点
def suspicous(arg1):
    if arg1>=1:
        #可配置参数，暂时1.2
        Ievent=1.2
        if arg1>=pmax*Ievent:
            return 1
    elif arg1<1:
        #可配置参数，暂时0.9
        Ievent=0.9
        if arg1>Ievent:
            return 1
#找出可疑事件
list_spnum=[]
for n,m in zip(range(0,len(Yi_event)),Yi_event):
    if suspicous(m):
        list_spnum.append(n)
list_spname=[]
for n in list_spnum:
    list_spname.append(list_eventname_set[n])

##############################################################################################################################################################

#sp_event=[]
#向analysis表里插入数据
for n,m in zip(list_spname,list_spnum):
    #使用exists检查是否存在相同数据，防止重复插入
    cur.execute('select id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period from open_event_data\
                where eventname="'+n+'\"'+' and period='+list_period_set[-1]+' and not exists(select * from analysis where  eventname="'\
                +n+'\"'+' and period='+list_period_set[-1]+')')
    sel=cur.fetchall()

    #analysis后面的列数和values后面的%s，以及和fetchall()返回结果里每个元组的项数相同
    #将从open_event_data表里选出的数据插入到analysis表里
    cur.executemany('insert into analysis(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                    values(%s,%s,%s,%s,%s,%s,%s,%s)',sel)
    #将事件详情插入到details表里
    cur.executemany('insert into details(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                    values(%s,%s,%s,%s,%s,%s,%s,%s)',sel)

#将ui_event_av和event_num为null的行填上
cur.execute('select ui_event_av,event_num from analysis where period='+list_period_set[-1]+' and event_num is null')
sel4=cur.fetchall()
if len(sel4)!=0:
    for n,m in zip(list_spname,list_spnum):
        cur.execute('update analysis set ui_event_av ='+str(Ui_event_av[m])+',event_num ='+str(Xi_event[m])+' where eventname="'+n+\
                    '\"'+' and period='+list_period_set[-1])
cur.execute('select count from details where period='+list_period_set[-1]+' and count is null')
sel4a=cur.fetchall()
if len(sel4a)!=0:
    for n,m in zip(list_spname,list_spnum):
        cur.execute('update details set count='+str(Xi_event[m]))
