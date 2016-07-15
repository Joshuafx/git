#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filname:B_calculate_Y.py

# 周期数Ncycle 目前先手动输入
# 当期业务总数量Nevent_sum
# √每个业务前N期报警数量Ui_event_av
# √当期每个业务报警数量Xi_event
# √每个业务的总历史数量SUMi_event
# √每个业务当期数量与前N期报警数量比值Yi_event=Xi_event/Ui_event_av

import MySQLdb
# conn=MySQLdb.Connect(host='10.6.96.64',user='root',passwd='123qweasd',db='event_history',port=3306)
conn = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='123456', db='event_history', port=3306)
cur = conn.cursor()

# 得到目前所有的period
cur.execute('select period from open_event_data')
all_period = cur.fetchall()
list_period = []
for n in all_period:
    list_period.append(n[0])
list_period_set = list(set(list_period))
list_period_set.sort()
len_period = len(list_period_set)

# 得到目前所有的business
cur.execute('select business from open_event_data')
all_business = cur.fetchall()
list_business = []
for n in all_business:
    list_business.append(n[0])
list_business_set = list(set(list_business))

# 计算Xi_event,当期每个业务报警数量
Xi_event = {}
for n in list_business_set:
    SQL = 'select ifnull(count(business),0) from open_event_data where business=\"' + n + '\"' + ' and period=' + \
          list_period_set[-1]
    cur.execute(SQL)
    Xi_event[n] = cur.fetchall()[0][0]

# 计算Ui_event_av,前几期均值
# Ncycle=input('请输入周期数：')
Ui_event = {}
Ui_event_av = {}
len_business = len(list_business_set)
for n in list_business_set:
    SQL = 'select ifnull(count(business),0) from open_event_data where business=\"' + n + '\"' + ' and period between ' + \
          list_period_set[0] + ' and ' + list_period_set[-2]
    cur.execute(SQL)
    Ui_event[n] = cur.fetchall()[0][0]
    Ui_event_av[n] = float(Ui_event[n]) / len_period

# 计算SUMi_event
SUMi_event = {}
for n in list_business_set:
    SQL = 'select ifnull(count(business),0) from open_event_data where business=\"' + n + '\"'
    cur.execute(SQL)
    SUMi_event[n]=cur.fetchall()[0][0]


# 根据Ui_event_av是否大于1，用不同的公式计算Y
def compare_1(arg1, n):
    if arg1 >= 1:
        return Xi_event[n] / Ui_event_av[n]
    elif arg1 < 1:
        return Xi_event[n] / SUMi_event[n]

# 求Yi_event
Yi_event = {}
for n in list_business_set:
    Yi_event[n]=(compare_1(Ui_event_av[n], n))