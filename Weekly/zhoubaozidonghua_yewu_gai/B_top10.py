#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:B_top10

from B_Suspicious_point import *
from B_calculate_Y import *

cur.execute('delete from business_top10 where period='+list_period_set[-1])

# 一线前十业务
SQL_ten_1 = 'select business,count(business) as business_num,period from open_event_data where period=' + \
            list_period_set[-1] + ' and eventoperator like "%一线%"' + \
            ' group by business order by count(business) desc limit 10'
cur.execute(SQL_ten_1)
sel = cur.fetchall()
business_top10 = []
for n in sel:
    business_top10.append(n[0])

for m in business_top10:
    cur.execute(
        'select id,business,eventname,ipaddress,happentime,eventoperator,period from open_event_data where business=\"' + m +'\" and period=' + \
        list_period_set[-1])
    sel2 = cur.fetchall()
    cur.executemany("insert into business_top10(id,business,eventname,ipaddress,happentime,eventoperator,period) values(%s,%s,%s,%s,%s,%s,%s)",sel2)
    cur.execute("update business_top10 set event_num="+str(Xi_event[m])+" where business=\""+m+"\" and period="+list_period_set[-1])
    cur.execute("update business_top10 set ui_event_av="+str(Ui_event_av[m])+"where business=\""+m+"\" and period="+list_period_set[-1])

# 二线前十业务
SQL_ten_2 = 'select business,count(business) as business_num,period from open_event_data where period=' + \
            list_period_set[-1] + ' and eventoperator="%二线%"' + \
            ' group by business order by count(business) desc limit 10'
cur.execute(SQL_ten_2)
sel3 = cur.fetchall()
business_top102 = []
for n in sel3:
    business_top102.append(n[0])

for m in business_top102:
    cur.execute(
        'select id,business,eventname,ipaddress,happentime,eventoperator,period from open_event_data where business=\"' + m +'\" and period=' + \
        list_period_set[-1])
    sel4 = cur.fetchall()
    cur.executemany("insert into business_top10(id,business,eventname,ipaddress,happentime,eventoperator,period) values(%s,%s,%s,%s,%s,%s,%s)",sel4)
    cur.execute("update business_top10 set event_num="+str(Xi_event[m])+" where business=\""+m+"\" and period="+list_period_set[-1])
    cur.execute("update business_top10 set ui_event_av="+str(Ui_event_av[m])+"where business=\""+m+"\" and period="+list_period_set[-1])

# conn.close()
