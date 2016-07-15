#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:B_Suspicious_point

# √置信水平Z，默认Z90
# √业务比值均值：Uevent_av
# √业务比值标准差：Sevent
# √区间估计上限：Pmax = Uevent-av + Z
# √区间估计下限：Pmin = Uevent-av - Z
# √Ievent高可疑异常点系数，可配置

# list_business_set:所有业务名称。Ui_event_av：每个业务前N期均值。Xi_event：当期每个业务报警数量。

from B_calculate_Y import *
# 写成函数，在weekly里调用

def USS(Yievent):
    Uevent_av = sum(Yievent.values()) / len(Yievent)
    SumY_sq = sum([(Yn - Uevent_av) ** 2 for Yn in Yievent.values()])
    Sevent = (SumY_sq / len(Yievent)) ** 0.5

# 正态分布表，置信水平为80%~99%
dict_Nd = {80: 1.28, 81: 1.31, 82: 1.34, 83: 1.37, 84: 1.41, \
           85: 1.44, 86: 1.48, 87: 1.51, 88: 1.55, 89: 1.60, \
           90: 1.64, 91: 1.69, 92: 1.75, 93: 1.81, 94: 1.88, \
           95: 1.96, 96: 2.05, 97: 2.17, 98: 2.32, 99: 2.58}

# 判断可疑点
def suspicous(arg1,Iabove,Ibelow,pmax):
    if arg1 >= 1:
        if arg1 >= pmax * Iabove:
            return 1
    elif arg1 < 1:
        if arg1 > Ibelow:
            return 1


# 找出可疑业务
def spname(Yievent,Iabove,Ibelow,pmax):
    list_spname = []
    for n, m in zip(Yievent.keys(), Yievent.values()):
        if suspicous(m,Iabove,Ibelow,pmax):
            list_spname.append(n)
    return  list_spname
#######################################################################################################################

# 向business_analysis表里插入数据
def insert_business_analysis(listspname,begin,end):
    for n in listspname:
    # 使用exists检查是否存在相同数据，防止重复插入
        cur.execute('select id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period from open_event_data\
                where business="' + n + '" and happentime between "'+str(begin)+'" and "'+str(end)+\
                '" and not exists(select * from business_analysis where  business="' + n + '" and happentime between "'+str(begin)+'" and "'+str(end)+'")')
        sel = cur.fetchall()

    # business_analysis后面的列数和values后面的%s，以及和fetchall()返回结果里每个元组的项数相同
    # 将从open_event_data表里选出的数据插入到business_analysis表里
        cur.executemany('insert into business_analysis(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                    values(%s,%s,%s,%s,%s,%s,%s,%s)', sel)

# 将最新一期的记录的status改为"新发生"
def update_status(begin,end):
    cur.execute('select id from business_analysis where status is null and happentime between "'+str(begin)+'" and "'+str(end)+'"')
    sel2 = cur.fetchall()
    if len(sel2) != 0:
        cur.execute('update business_analysis set status="新发生" where status is null and happentime between "'+str(begin)+'" and "'+str(end)+'"')

# 自动修改事件的tracing_num
def update_tracing_num():
    for n in list_business_set:
        cur.execute('select period from business_analysis where business="' + n + '\" and status!="已关闭"')
        sel5 = cur.fetchall()
        for m in range(0, len(sel5)):
            year_diff = int(list_period_set[-1][0:4]) - int(sel5[m][0][0:4])
            month_diff = int(list_period_set[-1][4:6]) - int(sel5[m][0][4:6])
            week_diff = int(list_period_set[-1][6:]) - int(sel5[m][0][6:])
            tracing_num = year_diff * 48 + month_diff * 4 + week_diff
            cur.execute('update business_analysis set tracing_num=' + str(tracing_num) + ' where status!="已关闭"')

# 修改事件的status
def change_status():
    cur.execute('select id from business_analysis where status="新发生" ' + 'and tracing_num>0')
    sel3 = cur.fetchall()
    if len(sel3) != 0:
        cur.execute('update business_analysis set status="进行中" where tracing_num>0 and status="新发生"')


# 将ui_event_av和event_num为null的行填上
def insert_av_num(listspname,Xievent,begin,end):
    cur.execute('select ui_event_av,event_num from business_analysis where happentime between "'+str(begin)+'" and "'+str(end) + '" and event_num is null')
    sel4 = cur.fetchall()
    if len(sel4) != 0:
        for n in listspname:
            cur.execute('update business_analysis set ui_event_av =' + str(Ui_event_av[n]) + ',event_num =' + str(
                Xievent[n]) + ' where business="' + n + '\"' + ' and happentime between "'+str(begin)+'" and "'+str(end)+'"')

# 填机器名关键词m_name_key，有缩写的取缩写，没有缩写的取整个
def insert_mkey(begin,end):
    cur.execute('select id,machinename from business_analysis WHERE m_name_key is NULL AND happentime between "'+str(begin)+'" and "'+str(end)+'"')
    sel6 = cur.fetchall()
    for n in sel6:
        m_name_key = n[1].split('-')[-1]
        sql = 'update business_analysis SET m_name_key ="' + m_name_key + '" where id =' + str(n[0])
        cur.execute(sql)

# 定义几个函数用于在weekly.py里调用，函数的参数就可以使用weekly.py里的参数了。
def YewuJizeng(begin,end):
    sql='select business,eventname,m_name_key,ipaddress,happentime,maintainlevel,ui_event_av,event_num,remark,id from business_analysis WHERE happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(sql)
    yewufin = cur.fetchall()
    return yewufin

def YewuXiangqing(business,begin,end):
    cur.execute('select business,eventname,machinename,ipaddress,happentime,maintainlevel,id from business_analysis where happentime between "'+str(begin)+'" and "'+str(end)+'" and business="'+str(business)+'"')
    sel7=cur.fetchall()
    YWxiangqing={}
    for i in sel7:
        YWxiangqing[i[-1]]=list(i)
    return YWxiangqing

#将business_data里的网页上的remark列encode('utf8')后再插入表
def Yewusave(business_data,begin,end):
    li=[]
    for i in business_data:
        cur.execute("select * FROM business_analysis WHERE id="+i[-1])
        sel8=cur.fetchall()[0]
        sel8=list(sel8)
        sel8[13]=i[8].encode('utf8')
        li.append(sel8)
    cur.execute('delete from business_analysis where happentime between "'+str(begin)+'" and "'+str(end)+'"')
    cur.executemany("insert into business_analysis values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",tuple(li))

def hisory_trace(begin,end):
    SQL="select status,period,business,eventname,ipaddress,happentime,maintainlevel,m_name_key,ui_event_av,event_num,finding,tracing_num,remark,id FROM business_analysis "+\
        'where happentime between "'+str(begin)+'" and "'+str(end)+'"'
    cur.execute(SQL)
    his_trc=cur.fetchall()
    return his_trc

# 回家调整数据库表，少列
def Yewuhissave(business_result,begin,end):
    for n in range(0,len(business_result)):
        for m in [0,2,3,10,12]:
            business_result[n][m]=business_result[n][m].encode('utf8')
    cur.execute('delete from business_historical_tracing where happentime between "'+str(begin)+'" and "'+str(end)+'"')
    SQL="insert into business_historical_tracing(status,period,business,eventname,ipaddress,happentime,maintainlevel,m_name_key,ui_event_av,event_num,finding,tracing_num,remark,id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(SQL,business_result)
# 将每块不同的功能的相应部分代码，分别写成函数的形式，调整调用关系。