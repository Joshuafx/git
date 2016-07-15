#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename:historical_tracing

from Suspicious_point import *
from calculate_Y import *

#向historical_tracing表里插数据
for n in list_spname:
    cur.execute('select eventname,happentime,business,period,ui_event_av,event_num from analysis where \
                eventname="'+n+'\"'+' and period='+list_period_set[-1]+' and not exists(select * from historical_tracing where\
                eventname="'+n+'\"'+' and period='+list_period_set[-1]+')'+' group by eventname')
    sel2=cur.fetchall()
    cur.executemany('insert into historical_tracing(eventname,happentime,business,period,ui_event_av,event_num) \
                    values(%s,%s,%s,%s,%s,%s)',sel2)

'''
#假设激增事件每期不超过100个，则ID改之前为小于100的自增数字，加上period*100后大于100，
#由此判断ID是否已修改成2015070201的格式，防止重复更新。
cur.execute('select id from historical_tracing where period='\
            +list_period_set[-1]+' and id<100')
sel3=cur.fetchall()
#使用IF判断只是为了防止代码重复执行，提高点效率
if len(sel3)!=0:
    cur.execute('update historical_tracing set id=id+'+\
                str(int(list_period_set[-1])*100)+",status='新发生'"+\
                ',tracing_num=0'+' where period='+list_period_set[-1]+\
                ' and id<100')
'''
cur.execute('select id from historical_tracing where status is null and period='+list_period_set[-1])
sel3=cur.fetchall()
if len(sel3)!=0:
    cur.execute('update historical_tracing set status="新发生" where status is null and period='+list_period_set[-1])
    
#自动修改事件的tracing_num
for n in list_eventname_set:
    cur.execute('select period from historical_tracing where eventname="'+n+'\" and status!="已关闭"')
    sel5=cur.fetchall()
    for m in range(0,len(sel5)):
        year_diff=int(list_period_set[-1][0:4])-int(sel5[m][0][0:4])
        month_diff=int(list_period_set[-1][4:6])-int(sel5[m][0][4:6])
        week_diff=int(list_period_set[-1][6:])-int(sel5[m][0][6:])
        tracing_num=year_diff*48+month_diff*4+week_diff
        cur.execute('update historical_tracing set tracing_num='+ str(tracing_num)+' where status!="已关闭"')
#修改事件的status
cur.execute('select * from historical_tracing where status="新发生" '+'and tracing_num>0')
sel8=cur.fetchall()
if len(sel8)!=0:
    cur.execute('update historical_tracing set status="进行中" where '+'tracing_num>0 and status!="已关闭"')

#将某类事件的所以IP填到historical_tracing里
cur.execute('select ipaddress from historical_tracing where period='+list_period_set[-1]+' and ipaddress is null')
sel7=cur.fetchall()
if len(sel7)!=0:
    for n in list_spname:
        #用group by去重复，order by...desc按数量降序排序
        cur.execute('select ipaddress,count(ipaddress) from analysis where eventname="'+n+'\"'+\
                ' and period='+list_period_set[-1]+' group by ipaddress order by count(ipaddress) desc')
        sel6=cur.fetchall()
        str_ev=''
        list_ev=[]
        for m in range(0,len(sel6)):
            list_ev.append(sel6[m][0])
        for l in range(0,len(list_ev)):
            str_ev=str_ev+list_ev[l]+','
        #去掉最后一个逗号
        str_ev=str_ev[:-1]
        cur.execute('update historical_tracing set ipaddress="'+str_ev+'" where eventname="'+n+'\"')

#cur.close()
#conn.close()