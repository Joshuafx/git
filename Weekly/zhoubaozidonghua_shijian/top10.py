#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename:top10

from Suspicious_point import *
from calculate_Y import *

#一线前十事件
SQL_ten_1='select eventname,count(eventname) as ev_num,period from open_event_data where period='+list_period_set[-1]+' and eventoperator="一线工程师"'+\
           ' group by eventname order by count(eventname) desc limit 10'
cur.execute(SQL_ten_1)
sel9=cur.fetchall()
SQL_ten_1a='select eventname,event_num,period from yixian_top10 where period='+list_period_set[-1]+' and eventoperator="一线工程师" order by event_num desc'
cur.execute(SQL_ten_1a)
sel9_a=cur.fetchall()
if sel9!=sel9_a:
    cur.execute('delete from yixian_top10 where period='+list_period_set[-1])
    cur.executemany('insert into yixian_top10(eventname,event_num,period) values(%s,%s,%s)',sel9)
    cur.execute('update yixian_top10 set eventoperator="一线工程师"')
    for x in range(0,10):
        cur.execute('select ipaddress,count(ipaddress) from open_event_data where eventname="'+sel9[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by ipaddress order by count(ipaddress) desc')
        sel_ip1=cur.fetchall()
        str_ip1=''
        list_ip1=[]
        for m in range(0,len(sel_ip1)):
            list_ip1.append(sel_ip1[m][0])
        for l in range(0,len(list_ip1)):
            str_ip1=str_ip1+list_ip1[l]+','
        #去掉最后一个逗号
        str_ip1=str_ip1[:-1]
        cur.execute('update yixian_top10 set ipaddress="'+str_ip1+'" where eventname="'+sel9[x][0]+'\"')
        ######
        cur.execute('select happentime,count(happentime) from open_event_data where eventname="'+sel9[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by happentime order by count(happentime) desc')
        sel_time1=cur.fetchall()
        str_time1=''
        list_time1=[]
        for m in range(0,len(sel_time1)):
            list_time1.append(sel_time1[m][0])
        for l in range(0,len(list_time1)):
            str_time1=str_time1+str(list_time1[l])+','
        str_time1=str_time1[:-1]
        cur.execute('update yixian_top10 set happentime="'+str_time1+'" where eventname="'+sel9[x][0]+'\"')
        ######
        cur.execute('select business,count(business) from open_event_data where eventname="'+sel9[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by business order by count(business) desc')
        sel_busi1=cur.fetchall()
        str_busi1=''
        list_busi1=[]
        for m in range(0,len(sel_busi1)):
            list_busi1.append(sel_busi1[m][0])
        for l in range(0,len(list_busi1)):
            str_busi1=str_busi1+list_busi1[l]+','
        str_busi1=str_busi1[:-1]
        cur.execute('update yixian_top10 set business="'+str_busi1+'" where eventname="'+sel9[x][0]+'\"')
        Ui_event_av10=list_eventname_set.index(sel9[x][0])
        cur.execute('update yixian_top10 set ui_event_av='+str(Ui_event_av[Ui_event_av10])+' where eventname="'+sel9[x][0]+'\"')
        
#二线前十
SQL_ten_2='select eventname,count(eventname) as ev_num,period from open_event_data where period='+list_period_set[-1]+' and eventoperator="二线工程师"'+\
           ' group by eventname order by count(eventname) desc limit 10'
cur.execute(SQL_ten_2)
sel10=cur.fetchall()
SQL_ten_2a='select eventname,event_num,period from yixian_top10 where period='+list_period_set[-1]+' and eventoperator="二线工程师" order by event_num desc'
cur.execute(SQL_ten_2a)
sel10_a=cur.fetchall()
if sel10!=sel10_a:
    cur.execute('delete from yixian_top10 where period='+list_period_set[-1])
    cur.executemany('insert into yixian_top10(eventname,event_num,period) values(%s,%s,%s)',sel10)
    cur.execute('update yixian_top10 set eventoperator="二线工程师"')
    for x in range(0,10):
        cur.execute('select ipaddress,count(ipaddress) from open_event_data where eventname="'+sel10[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by ipaddress order by count(ipaddress) desc')
        sel_ip2=cur.fetchall()
        str_ip2=''
        list_ip2=[]
        for m in range(0,len(sel_ip2)):
            list_ip2.append(sel_ip2[m][0])
        for l in range(0,len(list_ip2)):
            str_ip2=str_ip2+list_ip2[l]+','
        #去掉最后一个逗号
        str_ip1=str_ip2[:-1]
        cur.execute('update yixian_top10 set ipaddress="'+str_ip2+'" where eventname="'+sel10[x][0]+'\"')
        ######
        cur.execute('select happentime,count(happentime) from open_event_data where eventname="'+sel10[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by happentime order by count(happentime) desc')
        sel_time2=cur.fetchall()
        str_time2=''
        list_time2=[]
        for m in range(0,len(sel_time2)):
            list_time2.append(sel_time2[m][0])
        for l in range(0,len(list_time2)):
            str_time2=str_time2+str(list_time2[l])+','
        str_time1=str_time2[:-1]
        cur.execute('update yixian_top10 set happentime="'+str_time1+'" where eventname="'+sel10[x][0]+'\"')
        ######
        cur.execute('select business,count(business) from open_event_data where eventname="'+sel10[x][0]+'\"'+' and period='+list_period_set[-1]+\
                    ' group by business order by count(business) desc')
        sel_busi2=cur.fetchall()
        str_busi2=''
        list_busi2=[]
        for m in range(0,len(sel_busi2)):
            list_busi2.append(sel_busi2[m][0])
        for l in range(0,len(list_busi2)):
            str_busi2=str_busi2+list_busi2[l]+','
        str_busi2=str_busi2[:-1]
        cur.execute('update yixian_top10 set business="'+str_busi2+'" where eventname="'+sel10[x][0]+'\"')
        Ui_event_av10=list_eventname_set.index(sel10[x][0])
        cur.execute('update yixian_top10 set ui_event_av='+str(Ui_event_av[Ui_event_av10])+' where eventname="'+sel10[x][0]+'\"')

#cur.close()
#conn.close()