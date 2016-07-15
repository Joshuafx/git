#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:B_top10

from B_Suspicious_point import *

def topB_10(begin,end,Xi_event) :
    cur.execute('delete from business_top10 where happentime between "'+str(begin)+'" and "'+str(end)+'"')

    # 前十业务
    SQL_ten_1 = 'select business,count(business) as business_num,period from open_event_data where happentime between "'+str(begin)+\
                '" and "'+str(end) +'" group by business order by count(business) desc limit 10'
    cur.execute(SQL_ten_1)
    sel = cur.fetchall()
    business_top10 = []
    for n in sel:
        business_top10.append(n[0])

    for m in business_top10:
        SQL='select id,business,eventname,ipaddress,happentime,eventoperator,period from open_event_data where business="' + m +\
            '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL)
        sel2 = cur.fetchall()
        cur.executemany("insert into business_top10(id,business,eventname,ipaddress,happentime,eventoperator,period) values(%s,%s,%s,%s,%s,%s,%s)",sel2)
        SQL3='update business_top10 set event_num='+str(Xi_event[m])+' where business="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL3)
        SQL4='update business_top10 set ui_event_av='+str(Ui_event_av[m])+' where business="'+m+\
             '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
        cur.execute(SQL4)

def tongjiB(begin,end):
    tongjiB={}
    SQL='select business,event_num from business_top10 where happentime between "'+str(begin)+'" and "'+str(end)+'" group by business'
    cur.execute(SQL)
    sel5=list(cur.fetchall())
    name=[]
    value=[]
    for n in range(0,len(sel5)):
        sel5[n]=list(sel5[n])
        name.append(sel5[n][0])
        value.append(sel5[n][1])
    tongjiB['name']=name
    tongjiB['value']=value
    return tongjiB

# conn.close()