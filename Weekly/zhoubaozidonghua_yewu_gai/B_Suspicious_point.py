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

Uevent_av = sum(Yi_event.values()) / len(Yi_event)
SumY_sq = sum([(Yn - Uevent_av) ** 2 for Yn in Yi_event.values()])
Sevent = (SumY_sq / len(Yi_event)) ** 0.5

# 正态分布表，置信水平为80%~99%
dict_Nd = {80: 1.28, 81: 1.31, 82: 1.34, 83: 1.37, 84: 1.41, \
           85: 1.44, 86: 1.48, 87: 1.51, 88: 1.55, 89: 1.60, \
           90: 1.64, 91: 1.69, 92: 1.75, 93: 1.81, 94: 1.88, \
           95: 1.96, 96: 2.05, 97: 2.17, 98: 2.32, 99: 2.58}

# Z=dict_Nd[Z]*Uevent_av*Sevent
# Pmax = Uevent-av + Z
# Pmin = Uevent-av - Z
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

# 可配置参数，置信水平暂时设为90%
Conf_lv = 90
# Conf_lv=input('输入置信水平（80%~99%）：')
nd = dict_Nd[Conf_lv]
z = nd * Uevent_av * Sevent
pmax = Uevent_av + z
pmin = Uevent_av - z


# 判断可疑点
def suspicous(arg1):
    if arg1 >= 1:
        # 可配置参数，暂时1.2
        Ievent = 1.2
        if arg1 >= pmax * Ievent:
            return 1
    elif arg1 < 1:
        # 可配置参数，暂时0.9
        Ievent = 0.9
        if arg1 > Ievent:
            return 1


# 找出可疑业务
list_spname = []
for n, m in zip(Yi_event.keys(), Yi_event.values()):
    if suspicous(m):
        list_spname.append(n)
#######################################################################################################################

# 向business_analysis表里插入数据
for n in list_spname:
    # 使用exists检查是否存在相同数据，防止重复插入
    cur.execute('select id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period from open_event_data\
                where business="' + n + '\"' + ' and period=' + list_period_set[-1] +\
                ' and not exists(select * from business_analysis where  business="' + n + '\"' + ' and period=' + list_period_set[-1] + ')')
    sel = cur.fetchall()

    # business_analysis后面的列数和values后面的%s，以及和fetchall()返回结果里每个元组的项数相同
    # 将从open_event_data表里选出的数据插入到business_analysis表里
    cur.executemany('insert into business_analysis(id,eventname,machinename,ipaddress,happentime,business,maintainlevel,period) \
                    values(%s,%s,%s,%s,%s,%s,%s,%s)', sel)

# 将最新一期的记录的status改为"新发生"
cur.execute('select id from business_analysis where status is null and period=' + list_period_set[-1])
sel2 = cur.fetchall()
if len(sel2) != 0:
    cur.execute('update business_analysis set status="新发生" where status is null and period=' + list_period_set[-1])

# 自动修改事件的tracing_num
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
cur.execute('select id from business_analysis where status="新发生" ' + 'and tracing_num>0')
sel3 = cur.fetchall()
if len(sel3) != 0:
    cur.execute('update business_analysis set status="进行中" where tracing_num>0 and status="新发生"')


# 将ui_event_av和event_num为null的行填上
cur.execute('select ui_event_av,event_num from business_analysis where period=' + list_period_set[-1] + ' and event_num is null')
sel4 = cur.fetchall()
if len(sel4) != 0:
    for n in list_spname:
        cur.execute('update business_analysis set ui_event_av =' + str(Ui_event_av[n]) + ',event_num =' + str(
            Xi_event[n]) + ' where business="' + n + '\"' + ' and period=' + list_period_set[-1])

# 填机器名关键词m_name_key，有缩写的取缩写，没有缩写的去整个
cur.execute('select id,machinename from business_analysis WHERE m_name_key is NULL AND period='+list_period_set[-1])
sel6=cur.fetchall()
for n in sel6:
    key=n[1].split('-')[-1]
    sql='update business_analysis SET m_name_key ="'+key+'" where id ='+str(n[0])
    cur.execute(sql)


cur.execute('select business,eventname,m_name_key,ipaddress,happentime,maintainlevel,ui_event_av,event_num,remark,id from business_analysis WHERE period='+\
            list_period_set[-1])
yewufin=cur.fetchall()

