import MySQLdb

#��������
conn=MySQLdb.connect(host='10.6.96.64',user='root',passwd='123qweasd',\
                     db='event_history',port=3306)#charset='utf8'
cur=conn.cursor()
#cur.execute('set names gb2312')

#����ʮ��open_event_data��Ĳ�ѯ������ڲ���
cur.execute('select * from open_event_data limit 10')
sel_result=cur.fetchall()
print "����ʮ��open_event_data�����ݣ�\n",sel_result,'\n'

#��һ���б���ÿһ��
list_sel=[]
long_sel=len(sel_result)
for n in sel_result:
    list_sel.append(n)

print "���list_sel�б��ÿһ��"
for n in list_sel:
    print n,'\n'

#����open_event_data�����ݵ�txt�ĵ�
#cur.execute('use event_history')
#cur.execute('''select * into outfile "D:\\test\\test1.txt" fields terminated \
#by '|'lines terminated by '\r\n' from open_event_data''')

cur.execute('select * from open_event_data')
sel_result_all=cur.fetchall()
list_sel_all=[]
#��open_event_data������д�뵽���Լ���1��txt�ĵ���
f=open('open_event_data.txt','w')
f.write(str(sel_result_all))
f.close()
