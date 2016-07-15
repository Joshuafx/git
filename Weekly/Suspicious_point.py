#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:Suspicious_point

# √置信水平Z，默认Z90
# √事件比值均值：Uevent-av
# √事件比值标准差：Sevent
# √区间估计上限：Pmax = Uevent-av + Z
# √区间估计下限：Pmin = Uevent-av - Z
# √Ievent高可疑异常点系数，可配置

# list_eventname_set:所有事件名称。Ui_event_av：每个事件前N期均值。Xi_event：当期每个事件报警数量。

from calculate_Y import *

def USS(Yi_event):
    Uevent_av = sum(Yi_event) / len(Yi_event)
    SumY_sq = sum([(Yn - Uevent_av) ** 2 for Yn in Yi_event])
    Sevent = (SumY_sq / len(Yi_event)) ** 0.5

# 正态分布表，置信水平为80%~99%
dict_NdE = {80: 1.28, 81: 1.31, 82: 1.34, 83: 1.37, 84: 1.41, \
           85: 1.44, 86: 1.48, 87: 1.51, 88: 1.55, 89: 1.60, \
           90: 1.64, 91: 1.69, 92: 1.75, 93: 1.81, 94: 1.88, \
           95: 1.96, 96: 2.05, 97: 2.17, 98: 2.32, 99: 2.58}

# 判断可疑点
def suspicousE(arg1,Iabove,Ibelow,pmaxE):
    if arg1 >= 1:
        if arg1 >= pmaxE * Iabove:
            return 1
    elif arg1 < 1:
        if arg1 > Ibelow:
            return 1


# 找出可疑事件
def spnumE(YieventE,Iabove,Ibelow,pmaxE):
    list_spnum = []
    for n, m in zip(range(0, len(YieventE)), YieventE):
        if suspicousE(m,Iabove,Ibelow,pmaxE):
            list_spnum.append(n)
    return list_spnum
def spnameE(list_spnum):
    list_spname = []
    for n in list_spnum:
        list_spname.append(list_eventname_set[n])
    return list_spname

# #############################################################################################################################################################

# sp_event=[]
# 向analysis表里插入数据
def insert_analysis(listspname,listspnum,begin,end):
    for n, m in zip(listspname, listspnum):
        # 使用exists检查是否存在相同数据，防止重复插入
        SQL='select id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period from open_event_data where eventname="' +n +\
            '" and happentime between "'+str(begin)+'" and "'+str(end) + '" and not exists(select * from analysis where eventname="' +n +\
            '" and happentime between "'+str(begin)+'" and "' + str(end) + '")'

        cur.execute(SQL)
        sel = cur.fetchall()

        # analysis后面的列数和values后面的%s，以及和fetchall()返回结果里每个元组的项数相同
        # 将从open_event_data表里选出的数据插入到analysis表里
        cur.executemany('insert into analysis(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                        values(%s,%s,%s,%s,%s,%s,%s,%s)', sel)
        # 将事件详情插入到details表里
        cur.executemany('insert into details(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                        values(%s,%s,%s,%s,%s,%s,%s,%s)', sel)

# 将ui_event_av和event_num为null的行填上
def insert_av_numE(listspname,listspnum,XieventE,begin,end):
    cur.execute('select ui_event_av,event_num from analysis where period=' + list_period_set[-1] + ' and event_num is null')
    sel4 = cur.fetchall()
    if len(sel4) != 0:
        for n, m in zip(listspname, listspnum):
            SQL='update analysis set ui_event_av =' + str(Ui_event_av[m]) + ',event_num =' + str(XieventE[m]) + ' where eventname="' + n + \
                '" and happentime between "'+str(begin)+'" and "'+str(end)+'"'
            cur.execute(SQL)
    cur.execute('select count from details where happentime between "'+str(begin)+'" and "'+str(end)+'" and count is null')
    sel4a = cur.fetchall()
    if len(sel4a) != 0:
        for n, m in zip(listspname, listspnum):
            cur.execute('update details set count=' + str(XieventE[m]))

# 填机器名关键词m_name_key，有缩写的取缩写，没有缩写的取整个
def insert_mkeyE(begin,end):
    cur.execute('select id,machinename from analysis WHERE m_name_key is NULL AND happentime between "'+str(begin)+'" and "'+str(end)+'"')
    sel6 = cur.fetchall()
    for n in sel6:
        m_name_key = n[1].split('-')[-1]
        sql = 'update analysis SET m_name_key ="' + m_name_key + '" where id =' + str(n[0])
        cur.execute(sql)

def ShijianJizeng(begin,end):
    sql='select eventname,m_name_key,ipaddress,happentime,business,maintainlevel,ui_event_av,event_num,remark,id from analysis WHERE happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(sql)
    shijianfin = cur.fetchall()
    return shijianfin

def ShijianXiangqing(event,begin,end):
    cur.execute('select eventname,machinename,business,ipaddress,happentime,maintainlevel,id from analysis where happentime between "'+str(begin)+'" and "'+str(end)+'" and eventname="'+str(event)+'"')
    sel7=cur.fetchall()
    YWxiangqing={}
    for i in sel7:
        YWxiangqing[i[-1]]=list(i)
    return YWxiangqing

#将event_date里的网页上的remark列encode('utf8')后再插入表
def Shijiansave(event_date,begin,end):
    li=[]
    for i in event_date:
        cur.execute("select * FROM analysis WHERE id="+i[-1])
        sel8=cur.fetchall()[0]
        sel8=list(sel8)
        sel8[9]=i[8].encode('utf8')
        li.append(sel8)
    cur.execute('delete from analysis where happentime between "'+str(begin)+'" and "'+str(end)+'"')
    cur.executemany("insert into analysis values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",tuple(li))