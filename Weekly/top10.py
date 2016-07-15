#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:top10

from Suspicious_point import *

def top_10(begin,end,Xi_event):
    # 一线前十事件
    cur.execute('delete from yixian_top10 where happentime between "'+str(begin)+'" and "'+str(end)+'"')

    SQL_ten_1='select eventname,count(eventname) as ev_num,period from open_event_data where happentime between "'+str(begin)+\
              '" and "'+str(end)+'" and eventoperator like "%一线%"'+' group by eventname order by count(eventname) desc limit 10'
    cur.execute(SQL_ten_1)
    sel=cur.fetchall()
    event_top10 = []
    for n in sel:
        event_top10.append(n[0])
    for m,n in zip(event_top10,range(0,len(event_top10))):
        num=list_eventname_set.index(m)
        SQL='select id,business,eventname,ipaddress,happentime,eventoperator,period from open_event_data where eventname="' + m +\
            '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL)
        sel2 = cur.fetchall()
        cur.executemany("insert into yixian_top10(id,business,eventname,ipaddress,happentime,eventoperator,period) values(%s,%s,%s,%s,%s,%s,%s)",sel2)
        SQL2='update yixian_top10 set event_num='+str(Xi_event[num])+' where eventname="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL2)
        SQL3='update yixian_top10 set ui_event_av='+str(Ui_event_av[num])+' where eventname="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL3)

    # 二线前十
    SQL_ten_2='select eventname,count(eventname) as ev_num,period from open_event_data where happentime between "'+str(begin)+\
              '" and "'+str(end)+'" and eventoperator not like "%一线%"'+' group by eventname order by count(eventname) desc limit 10'
    cur.execute(SQL_ten_2)
    sel=cur.fetchall()
    event_top10_2 = []
    for n in sel:
        event_top10_2.append(n[0])

    for m,n in zip(event_top10_2,range(0,len(event_top10_2))):
        SQL='select id,business,eventname,ipaddress,happentime,eventoperator,period from open_event_data where eventname="' + m +\
            '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL)
        sel2 = cur.fetchall()
        cur.executemany("insert into yixian_top10(id,business,eventname,ipaddress,happentime,eventoperator,period) values(%s,%s,%s,%s,%s,%s,%s)",sel2)
        SQL2='update yixian_top10 set event_num='+str(Xi_event[n-10])+' where eventname="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL2)
        Ui_num=list_eventname_set.index(m)
        SQL3='update yixian_top10 set ui_event_av='+str(Ui_event_av[Ui_num])+' where eventname="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL3)

def tongji1(begin,end):
    tongji1={}
    SQL='select eventname,event_num from yixian_top10 where eventoperator like "%一线%" and happentime between "'+str(begin)+'" and "'+str(end)+\
        '" group by eventname'
    cur.execute(SQL)
    sel5=list(cur.fetchall())
    name=[]
    value=[]
    for n in range(0,len(sel5)):
        sel5[n]=list(sel5[n])
        name.append(sel5[n][0])
        value.append(sel5[n][1])
    tongji1['name']=name
    tongji1['value']=value
    return tongji1

def tongji2(begin,end):
    tongji2={}
    SQL2='select eventname,event_num from yixian_top10 where eventoperator not like "%一线%" and happentime between "'+str(begin)+'" and "'+str(end)+\
         '" group by eventname'
    cur.execute(SQL2)
    sel5=list(cur.fetchall())
    name=[]
    value=[]
    for n in range(0,len(sel5)):
        sel5[n]=list(sel5[n])
        name.append(sel5[n][0])
        value.append(sel5[n][1])
    tongji2['name']=name
    tongji2['value']=value
    return tongji2

# 帕累托图
# 不分一二线，前十报警
def Pareto(begin,end):
    SQL='select eventname,count(eventname) from open_event_data where happentime between "'+\
        str(begin)+'" and "'+str(end)+'" group by eventname order by count(eventname) desc limit 10'
    cur.execute(SQL)
    sel=cur.fetchall()
    seldict={}
    for n in sel:
        seldict[n[0]]=n[1]
    # 按值排序
    sortdict=sorted(seldict.iteritems(),key=lambda dic:dic[1],reverse=True)
    event=[]
    value=[]
    for m in sortdict:
        event.append(m[0])
        value.append(m[1])
    # 报警总数
    SQL2='select count(*) from open_event_data where happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(SQL2)
    sel2=cur.fetchall()
    sumevent=sel2[0][0]*1.0
    # 计算“其他”
    event.append('其他')
    value.append(sumevent-sum(value))
    # 累积频数
    percent=[]
    for x in range(1,12):
        a=sum(value[0:x])*1.0
        b=a/sumevent
        c=round(b,4)*100  # 保留4位小数，并变成百分制
        percent.append(c)
    pareto={}
    pareto['name']=event
    pareto['value1']=value
    pareto['value2']=percent

    return pareto

def Core_Business(begin,end):
    SQL='select DISTINCT DATE_FORMAT(happentime,"%Y%-%m-%d") as day from open_event_data where happentime between "'+\
        str(begin)+'" and "'+str(end)+'" order by day'
    cur.execute(SQL)
    date=cur.fetchall()
    dates=[]
    for d in date:
        dates.append(d[0])
    print dates
    openet=[]
    openav=[]
    peizai=[]
    for d in dates:
        SQL2='select count(*) from open_event_data where DATE_FORMAT(happentime,"%Y%-%m-%d")="'+str(d)+'" and business like '
        cur.execute(SQL2+'"%openet%"')
        et=cur.fetchall()[0][0]
        openet.append(et)
        cur.execute(SQL2+'"%openav%"')
        av=cur.fetchall()[0][0]
        openav.append(av)
        cur.execute(SQL2+'"%配载%"')
        pz=cur.fetchall()[0][0]
        peizai.append(pz)
    print openet,openav,peizai
    Cbusiness={}
    Cbusiness['name']=dates
    Cbusiness['value1']=openet
    Cbusiness['value2']=openav
    Cbusiness['value3']=peizai

    return Cbusiness

#cur.close()
#conn.close()