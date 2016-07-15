import MySQLdb

#建立连接
conn=MySQLdb.connect(host='10.6.96.64',user='root',passwd='123qweasd',\
                     db='event_history',port=3306)#charset='utf8'
cur=conn.cursor()
#cur.execute('set names gb2312')

#返回十行open_event_data表的查询结果用于测试
cur.execute('select * from open_event_data limit 10')
sel_result=cur.fetchall()
print "返回十行open_event_data表数据：\n",sel_result,'\n'

#用一个列表保存每一行
list_sel=[]
long_sel=len(sel_result)
for n in sel_result:
    list_sel.append(n)

print "输出list_sel列表的每一项"
for n in list_sel:
    print n,'\n'

#导出open_event_data表数据到txt文档
#cur.execute('use event_history')
#cur.execute('''select * into outfile "D:\\test\\test1.txt" fields terminated \
#by '|'lines terminated by '\r\n' from open_event_data''')

cur.execute('select * from open_event_data')
sel_result_all=cur.fetchall()
list_sel_all=[]
#将open_event_data表数据写入到我自己的1个txt文档里
f=open('open_event_data.txt','w')
f.write(str(sel_result_all))
f.close()
