#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:conf_his.py

import MySQLdb
# conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
conn = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='123456', db='event_history', port=3306)
cur = conn.cursor()

# 保存配置项
def save_conf(starttime,endtime,compare,confidence,above,below):
    conf=[starttime,endtime,compare,confidence,above,below]
    start=starttime.split(' ')[0]
    SQLdelete='delete from conf_his where DATE_FORMAT(begintime,"%Y-%m-%d")="'+str(start)+'"'
    cur.execute(SQLdelete)
    SQL='insert into conf_his(begintime,endtime,comp,confi,ab,bel) values(%s,%s,%s,%s,%s,%s)'
    cur.execute(SQL,conf)
    conn.commit()

# 返回事件历史数据标题
def sel_event_conf():
    cur.execute('select DATE_FORMAT(begintime,"%Y%m%d"),DATE_FORMAT(endtime,"%Y%m%d") from conf_his')
    sel=cur.fetchall()
    time=[]
    for n in sel:
        start=str(n[0])
        happen=start[0:4]+'-'+start[4:6]+'-'+start[6:]
        end=str(n[1])
        finish=end[0:4]+'-'+end[4:6]+'-'+end[6:]
        cur.execute('select id from analysis where DATE_FORMAT(happentime,"%Y-%m-%d") between"'+happen+'" and "'+finish+'"')
        sel=cur.fetchall()
        if len(sel)!=0:
            chatime=start+'-'+end
            time.append(chatime)
    return time

# 删除事件历史数据及事件详情
def delete_cof_event(event_delete):
    for n in event_delete:
        a=n.split('-')[0]
        begintime=a[0:4]+'-'+a[4:6]+'-'+a[6:]
        b=n.split('-')[1]
        endtime=b[0:4]+'-'+b[4:6]+'-'+b[6:]
        SQLdeljizeng='delete from analysis where DATE_FORMAT(happentime,"%Y-%m-%d") between"'+begintime+'" and "'+endtime+'"'
        cur.execute(SQLdeljizeng)
        SQLdeldet='delete from details where DATE_FORMAT(happentime,"%Y-%m-%d") between"'+begintime+'" and "'+endtime+'"'
        cur.execute(SQLdeldet)
        conn.commit()

# 将sel_event_conf和delete_cof_event修改成业务的