#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:historical_tracing

from Suspicious_point import *

# 向historical_tracing表里插数据
def insert_his_tracingE(begin,end):
    SQLid='select id from analysis where happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(SQLid)
    selid=cur.fetchall()
    selidlist=[]
    for n in selid:
        selidlist.append(n[0])
    for n in selidlist:
        SQL='select id,period,eventname,ipaddress,happentime,business,maintainlevel,m_name_key,ui_event_av,event_num from analysis where id=' \
            + str(n)+' and happentime between "'+str(begin)+'" and "'+str(end)+'" and not exists(select * from historical_tracing where id=' \
            + str(n)+' and happentime between "'+str(begin)+'" and "'+str(end)+'")'
        cur.execute(SQL)
        sel2 = cur.fetchall()
        cur.executemany('insert into historical_tracing(id,period,eventname,ipaddress,happentime,business,maintainlevel,m_name_key,ui_event_av,event_num) \
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', sel2)
    cur.execute('select id from historical_tracing where status is null and happentime between "' + str(begin) + '" and "' + str(end) + '"')
    sel3 = cur.fetchall()
    if len(sel3) != 0:
        cur.execute('update historical_tracing set status="新发生" where status is null and happentime between "' + str(begin) + '" and "' + str(end) + '"')

# 自动修改事件的tracing_num
def update_tracingE():
    for n in list_eventname_set:
        cur.execute('select period from historical_tracing where eventname="' + n + '\" and status!="已关闭"')
        sel5 = cur.fetchall()
        for m in range(0, len(sel5)):
            year_diff = int(list_period_set[-1][0:4]) - int(sel5[m][0][0:4])
            month_diff = int(list_period_set[-1][4:6]) - int(sel5[m][0][4:6])
            week_diff = int(list_period_set[-1][6:]) - int(sel5[m][0][6:])
            tracing_num = year_diff * 48 + month_diff * 4 + week_diff
            cur.execute('update historical_tracing set tracing_num=' + str(tracing_num) + ' where status!="已关闭"')
    # 修改事件的status
    cur.execute('select * from historical_tracing where status="新发生" ' + 'and tracing_num>0')
    sel8 = cur.fetchall()
    if len(sel8) != 0:
        cur.execute('update historical_tracing set status="进行中" where ' + 'tracing_num>0 and status!="已关闭"')

def event_trace(begin,end):
    SQL="select status,period,eventname,ipaddress,happentime,business,maintainlevel,m_name_key,ui_event_av,event_num,finding,tracing_num,remark,id FROM historical_tracing "+\
        'where happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(SQL)
    event_trc=cur.fetchall()
    return event_trc

# 回家调整数据库表，少列
def Shijianhissave(event_result,begin,end):
    for n in range(0,len(event_result)):
        for m in [0,2,5,10,12]:
            event_result[n][m]=event_result[n][m].encode('utf8')
    cur.execute('delete from historical_tracing where happentime between "'+str(begin)+'" and "'+str(end)+'"')
    SQL="insert into historical_tracing(status,period,eventname,ipaddress,happentime,business,maintainlevel,m_name_key,ui_event_av,event_num,finding,tracing_num,remark,id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(SQL,event_result)
'''
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
'''
# cur.close()
# conn.close()
