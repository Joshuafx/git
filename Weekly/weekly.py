# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, request, jsonify, url_for, redirect
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
cache = SimpleCache()

from B_top10 import *
from historical_tracing import *
from top10 import *
from conf_his import *
# 主页
@app.route('/', methods=['POST', 'GET'])
def index_page():
    return render_template('index.html')


# 配置参数页面
starttime=''
endtime=''
@app.route('/config', methods=['POST', 'GET'])
def config_page():
    # 尝试提取参数缓存
    config = []
    config.append(cache.get('startime'))
    config.append(cache.get('endtime'))
    config.append(cache.get('compare'))
    config.append(cache.get('confidence'))
    config.append(cache.get('above'))
    config.append(cache.get('below'))

    filttime1 = cache.get('filttime1')
    filttime2 = cache.get('filttime2')
    filtevent = cache.get('filtevent')
    filtip = cache.get('filtip')
    global starttime,endtime
    starttime=config[0]
    endtime=config[1]

    return render_template('config.html', config=config, filttime1=filttime1, filttime2=filttime2, filtevent=filtevent,
                           filtip=filtip)


# 获取配置参数并加入缓存
Jizengyewu=[]
@app.route('/getConfig', methods=['POST', 'GET'])
def getConfig():
    starttime = request.form.get('startime')  # 开始时间
    endtime = request.form.get('endtime')  # 结束时间
    compare = request.form.get('compare')  # 比较
    confidence = request.form.get('confidence')  # 执行水平
    above = request.form.get('above')
    below = request.form.get('below')

    save_conf(starttime,endtime,compare,confidence,above,below)

    number = len(request.form)  # url长度

    filttime1 = []  # 剔除开始时间
    filttime2 = []  # 剔除结束时间
    filtevent = []  # 剔除事件
    filtip = []  # 剔除ip

    for i in range(1, number - 5):
        time1 = "startime" + str(i)
        time2 = "endtime" + str(i)
        event = "event" + str(i)
        ip = "ip" + str(i)
        if request.form.get(time1, 'noValue') != 'noValue':
            filttime1.append(request.form.get(time1))
            filttime2.append(request.form.get(time2))
        if request.form.get(event, 'noValue') != 'noValue':
            filtevent.append(request.form.get(event))
        if request.form.get(ip, 'noValue') != 'noValue':
            filtip.append(request.form.get(ip))

    # 设置参数缓存
    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

# 业务相关计算
    print starttime,endtime
    Xi_event=Xi(starttime,endtime)
    Yi_event=Yi(Xi_event)
    Uevent_av = sum(Yi_event.values()) / len(Yi_event)
    SumY_sq = sum([(Yn - Uevent_av) ** 2 for Yn in Yi_event.values()])
    Sevent = (SumY_sq / len(Yi_event)) ** 0.5
    nd = dict_Nd[int(confidence)]
    z = nd * Uevent_av * Sevent
    pmax = Uevent_av + z
    pmin = Uevent_av - z
# 事件相关计算
    Xi_eventE=XiE(starttime,endtime)
    Yi_eventE=YiE(Xi_eventE)
    Uevent_avE = sum(Yi_eventE) / len(Yi_eventE)
    SumY_sqE = sum([(Yn - Uevent_avE) ** 2 for Yn in Yi_eventE])
    SeventE = (SumY_sqE / len(Yi_eventE)) ** 0.5
    ndE = dict_NdE[int(confidence)]
    zE = ndE * Uevent_avE * SeventE
    pmaxE = Uevent_avE + zE
    pminE = Uevent_avE - zE

# 有时间把下面的分别写成1个函数
# 业务相关计算
    list_spname=spname(Yi_event,float(above),float(below),pmax)
    insert_business_analysis(list_spname,starttime,endtime)
    update_status(starttime,endtime)
    update_tracing_num()
    change_status()
    insert_av_num(list_spname,Xi_event,starttime,endtime)
    insert_mkey(starttime,endtime)
    topB_10(starttime,endtime,Xi_event)
# 事件相关计算
    list_spnumE=spnumE(Yi_eventE,float(above),float(below),pmaxE)
    list_spnameE=spnameE(list_spnumE)
    insert_analysis(list_spnameE,list_spnumE,starttime,endtime)
    insert_av_numE(list_spnameE,list_spnumE,Xi_eventE,starttime,endtime)
    insert_mkeyE(starttime,endtime)
    top_10(starttime,endtime,Xi_eventE)

    global Jizengyewu
    Jizengyewu=YewuJizeng(starttime,endtime)

    return redirect(url_for('config_page'))

# 以事件类型为主的报警量激增列表
# 请求以事件类型为主的报警量激增列表
@app.route('/event_table', methods=['POST', 'GET'])
def event_table():
    testdata = ShijianJizeng(starttime,endtime)
    return render_template('event_table.html', event_data=testdata)


# 点击事件弹出该IP详细报警信息
@app.route('/event_detail', methods=['POST', 'GET'])
def event_detail():
    event = request.form.get('event')
    testdata = {}
    for i in range(1, 10):
        testdata[str(i)] = ['文件系统使用率超阀值' + str(i), 'vmaas-JBS' + str(i), '国际运价搜索' + str(i), '10.6.10.1' + str(i),
                            '2016-01-02' + str(i), 'S2' + str(i), i]
    return jsonify(testdata)


# 删除以事件类型为主的报警量激增列表中的项
@app.route('/event_delete', methods=['POST', 'GET'])
def event_delete():
    lengths = request.form.get('rows')
    event_data = []
    for n in range(0, int(lengths)):
        if request.form.get('event' + str(n)):
            row = []
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            event_data.append(row)
    Shijiansave(event_data,starttime,endtime)
    return render_template('event_table.html', event_data=event_data)


# 保存以事件类型为主的报警量激增列表
@app.route('/event_save_data', methods=['POST', 'GET'])
def event_save_data():
    lengths = request.form.get('rows')
    event_data = []
    for n in range(0, int(lengths)):
        if request.form.get('event' + str(n)):
            row = []
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            event_data.append(row)
    Shijiansave(event_data,starttime,endtime)
    return render_template('event_table.html', event_data=event_data)


# 提交以事件类型为主的报警量激增列表并返回历史事件追踪表
@app.route('/event_result', methods=['POST', 'GET'])
def event_result():
    insert_his_tracingE(starttime,endtime)
    update_tracingE()
    lengths = request.form.get('rows')
    event_data = []
    for n in range(0, int(lengths)):
        if request.form.get('event' + str(n)):
            row = []
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            event_data.append(row)
    testdata = event_trace(starttime,endtime)
    return render_template('event_result.html', event_result=testdata)


# 删除历史事件追踪表中的项
@app.route('/event_result_delete', methods=['POST', 'GET'])
def event_result_delete():
    lengths = request.form.get('rows')
    event_result = []
    for n in range(0, int(lengths)):
        if request.form.get('event' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            event_result.append(row)
    Shijianhissave(event_result,starttime,endtime)
    return render_template('event_result.html', event_result=event_result)


# 保存历史事件追踪表
@app.route('/event_save_result', methods=['POST', 'GET'])
def event_save_result():
    lengths = request.form.get('rows')
    event_result = []
    for n in range(0, int(lengths)):
        if request.form.get('event' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            event_result.append(row)
    Shijianhissave(event_result,starttime,endtime)
    return render_template('event_result.html', event_result=event_result)


# 以IP为主的报警量激增列表
# 请求以IP为主的报警量激增列表
@app.route('/ip_table', methods=['POST', 'GET'])
def ip_table():
    testdata = []
    for i in range(0, 65):
        testdata.append(
            ['10.6.1.1' + str(i), 'vwalaa' + str(i), 'cpu使用率高' + str(i), '2015-03-03 10:00', 'openav' + str(i),
             's4' + str(i), '1' + str(i), '2' + str(i), '已添加' + str(i), i])
    return render_template('ip_table.html', ip_data=testdata)


# 点击IP弹出该IP详细报警信息
@app.route('/ip_detail', methods=['POST', 'GET'])
def ip_detail():
    Ip = request.form.get('ip')
    testdata = {}
    for i in range(1, 10):
        testdata[str(i)] = ['10.6.1.1' + str(i), 'vmaas-JBS' + str(i), '国际运价搜索' + str(i), '文件系统使用率超阀值' + str(i),
                            '2016-01-02' + str(i), 'S2' + str(i), i]
    return jsonify(testdata)


# 删除以IP为主的报警量激增列表中的项
@app.route('/ip_delete', methods=['POST', 'GET'])
def ip_delete():
    lengths = request.form.get('rows')
    ip_data = []
    for n in range(0, int(lengths)):
        if request.form.get('ip' + str(n)):
            row = []
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            ip_data.append(row)
    return render_template('ip_table.html', ip_data=ip_data)


# 保存以IP为主的报警量激增列表
@app.route('/ip_save_data', methods=['POST', 'GET'])
def ip_save_data():
    lengths = request.form.get('rows')
    ip_data = []
    for n in range(0, int(lengths)):
        if request.form.get('ip' + str(n)):
            row = []
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            ip_data.append(row)
    return render_template('ip_table.html', ip_data=ip_data)


# 提交以IP为主的报警量激增列表并返回历史激增IP报警追踪表
@app.route('/ip_result', methods=['POST', 'GET'])
def ip_result():
    lengths = request.form.get('rows')
    ip_data = []
    for n in range(0, int(lengths)):
        if request.form.get('ip' + str(n)):
            row = []
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            ip_data.append(row)
    testdata = []
    for i in range(0, 65):
        testdata.append(['进行中', '201503' + str(i), '10.6.1.1' + str(i), '光纤交换机端口状态offline' + str(i), '几乎每天' + str(i),
                         '海航B2C' + str(i), 'S3' + str(i), 'VM11-TODE' + str(i), '1' + str(i), '3' + str(i),
                         '分析完毕' + str(i), '0' + str(i), '添加备注' + str(i), i])
    return render_template('ip_result.html', ip_result=testdata)


# 删除历史激增IP报警追踪表中的项
@app.route('/ip_result_delete', methods=['POST', 'GET'])
def ip_result_delete():
    lengths = request.form.get('rows')
    ip_result = []
    for n in range(0, int(lengths)):
        if request.form.get('ip' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            ip_result.append(row)
    return render_template('ip_result.html', ip_result=ip_result)


# 保存历史激增IP报警追踪表
@app.route('/ip_save_result', methods=['POST', 'GET'])
def ip_save_result():
    lengths = request.form.get('rows')
    ip_result = []
    for n in range(0, int(lengths)):
        if request.form.get('ip' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            ip_result.append(row)
    return render_template('ip_result.html', ip_result=ip_result)


# 以业务为主的报警量激增列表
# 请求以业务为主的报警量激增列表
@app.route('/business_table', methods=['POST', 'GET'])
def business_table():
    testdata = Jizengyewu
    return render_template('business_table.html', business_data=testdata)


# 点击业务弹出该业务详细报警信息
# 字典用什么当key？
@app.route('/business_detail', methods=['POST', 'GET'])
def business_detail():
    business = request.form.get('business')
    testdata = YewuXiangqing(business)
    return jsonify(testdata)


# 删除以业务为主的报警量激增列表中的项
@app.route('/business_delete', methods=['POST', 'GET'])
def business_delete():
    lengths = request.form.get('rows')
    business_data = []
    for n in range(0, int(lengths)):
        if request.form.get('business' + str(n)):
            row = []
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            business_data.append(row)
    Yewusave(business_data,starttime,endtime)
    return render_template('business_table.html', business_data=business_data)


# 保存以业务为主的报警量激增列表
# 这个函数里面调用我的Yewusave函数，使用business_data里返回的主键
@app.route('/business_save_data', methods=['POST', 'GET'])
def business_save_data():
    lengths = request.form.get('rows')
    business_data = []
    for n in range(0, int(lengths)):
        if request.form.get('business' + str(n)):
            row = []
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            business_data.append(row)
    Yewusave(business_data,starttime,endtime)
    return render_template('business_table.html', business_data=business_data)


# 提交以业务为主的报警量激增列表并返回历史激增IP报警追踪表
# 这里的business_data什么意义？
@app.route('/business_result', methods=['POST', 'GET'])
def business_result():
    lengths = request.form.get('rows')
    business_data = []
    for n in range(0, int(lengths)):
        if request.form.get('business' + str(n)):
            row = []
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            business_data.append(row)
    testdata = hisory_trace(starttime,endtime)
    return render_template('business_result.html', business_result=testdata)


# 删除历史业务追踪表中的项
@app.route('/business_result_delete', methods=['POST', 'GET'])
def business_result_delete():
    lengths = request.form.get('rows')
    business_result = []
    for n in range(0, int(lengths)):
        if request.form.get('business' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            business_result.append(row)
    Yewuhissave(business_result,starttime,endtime)
    return render_template('business_result.html', business_result=business_result)


# 保存历史业务追踪表
@app.route('/business_save_result', methods=['POST', 'GET'])
def business_save_result():
    lengths = request.form.get('rows')
    business_result = []
    for n in range(0, int(lengths)):
        if request.form.get('business' + str(n)):
            row = []
            row.append(request.form.get('status' + str(n)))
            row.append(request.form.get('order' + str(n)))
            row.append(request.form.get('business' + str(n)))
            row.append(request.form.get('event' + str(n)))
            row.append(request.form.get('ip' + str(n)))
            row.append(request.form.get('date' + str(n)))
            row.append(request.form.get('level' + str(n)))
            row.append(request.form.get('machine' + str(n)))
            row.append(request.form.get('average' + str(n)))
            row.append(request.form.get('values' + str(n)))
            row.append(request.form.get('final' + str(n)))
            row.append(request.form.get('first' + str(n)))
            row.append(request.form.get('mark' + str(n)))
            row.append(request.form.get('key' + str(n)))
            business_result.append(row)
    Yewuhissave(business_result,starttime,endtime)
    return render_template('business_result.html', business_result=business_result)


# 基本信息表
@app.route('/basic_table', methods=['post', 'get'])
def basic_table():
    testdata = [1352, 193.1, 122.4, 70.7, '95.0%', '5%', 1380, -28]
    return render_template('basic_table.html', basic_data=testdata)


# 删除基本信息表中的项
@app.route('/basic_delete', methods=['POST', 'GET'])
def basic_delete():
    basic_data = []
    basic_data.append(request.form.get('total'))
    basic_data.append(request.form.get('everyday'))
    basic_data.append(request.form.get('day'))
    basic_data.append(request.form.get('night'))
    basic_data.append(request.form.get('first'))
    basic_data.append(request.form.get('second'))
    basic_data.append(request.form.get('last'))
    basic_data.append(request.form.get('compare'))
    return render_template('basic_table.html', basic_data=basic_data)


# 保存基本信息表
@app.route('/basic_save', methods=['POST', 'GET'])
def basic_save():
    basic_data = []
    basic_data.append(request.form.get('total'))
    basic_data.append(request.form.get('everyday'))
    basic_data.append(request.form.get('day'))
    basic_data.append(request.form.get('night'))
    basic_data.append(request.form.get('first'))
    basic_data.append(request.form.get('second'))
    basic_data.append(request.form.get('last'))
    basic_data.append(request.form.get('compare'))
    return render_template('basic_table.html', basic_data=basic_data)


# 历史原始数据
@app.route('/history_data', methods=['POST', 'GET'])
def history_data():
    ip = []
    event = sel_event_conf()
    business = sel_event_conf()
    for i in range(0, 25):
        ip.append('20150311-20150317-' + str(i))
    testdata = [event,ip,business]
    return render_template('history_data.html', history_data=testdata)


# 删除原始数据
@app.route('/history_data_delete', methods=['POST', 'GET'])
def history_data_delete():
    row_event = request.form.get('rows_event')
    row_ip = request.form.get('rows_ip')
    row_business = request.form.get('rows_business')
    event_delete = []
    ip_delete = []
    business_delete = []

    ip = []
    business = []
    for i in range(0, int(row_event)):
        if request.form.get('event' + str(i)):
            event_delete.append(request.form.get('event' + str(i)))
    for i in range(0, int(row_ip)):
        if request.form.get('ip' + str(i)):
            ip_delete.append(request.form.get('ip' + str(i)))
    for i in range(0, int(row_business)):
        if request.form.get('business' + str(i)):
            business_delete.append(request.form.get('business' + str(i)))

    delete_cof_event(event_delete)
    event = sel_event_conf()
    for i in range(0, 15):
        ip.append('20150311-20150317-' + str(i))
        business.append('20150323-20150329-' + str(i))

    testdata = [event, ip , business]
    return render_template('history_data.html', history_data=testdata)


# 打开事件原始数据
@app.route('/history_data_event', methods=['POST', 'GET'])
def history_data_event():
    table_name = request.form.get('table_name');
    testdata = []
    for i in range(0, 30):
        testdata.append(['jboss服务器端口连接数高' + str(i), 'vwalaa' + str(i), '122.119.122.1' + str(i), '2015-03-03 10:00',
                         'openav' + str(i), 's4' + str(i), '1' + str(i), '2' + str(i), '已添加' + str(i), i])

    starttime = '2015-01-02'
    endtime = '2015-03-01'
    compare = '6'
    confidence = '0.9'
    above = '0.6'
    below = '0.6'
    filttime1 = ['2015-01-01', '2015-02-01', '2015-03-01']
    filttime2 = ['2-15-01-05', '2015-02-05', '2015-03-05']
    filtevent = ['cpu使用率高', '文件系统使用率超阀值']
    filtip = ['10.6.1.1', '10.6.137.1']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('event_table.html', event_data=testdata, config_data=configs, time1=filttime1,
                           time2=filttime2, events=filtevent, ips=filtip)


# 打开IP原始数据
@app.route('/history_data_ip', methods=['POST', 'GET'])
def history_data_ip():
    table_name = request.form.get('table_name');

    testdata = []
    for i in range(0, 13):
        testdata.append(
            ['10.6.1.1' + str(i), 'vwalaa' + str(i), 'cpu使用率高' + str(i), '2015-03-03 10:00', 'openav' + str(i),
             's4' + str(i), '1' + str(i), '2' + str(i), '已添加' + str(i), i])

    starttime = '123'
    endtime = '456'
    compare = '7'
    confidence = '8'
    above = 'nn'
    below = 'mm'
    filttime1 = [33]
    filttime2 = [44]
    filtevent = ['ttt']
    filtip = ['bbbb']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('ip_table.html', ip_data=testdata, config_data=configs, time1=filttime1, time2=filttime2,
                           events=filtevent, ips=filtip)


# 打开业务原始数据
@app.route('/history_data_business', methods=['POST', 'GET'])
def history_data_business():
    table_name = request.form.get('table_name');

    testdata = []
    for i in range(0, 14):
        testdata.append(
            ['openav' + str(i), 'cpu使用率高' + str(i), 'vwalaa' + str(i), '10.6.1.1' + str(i), '2015-03-03 10:00',
             's4' + str(i), '1' + str(i), '2' + str(i), '已添加' + str(i), i])

    starttime = '123'
    endtime = '456'
    compare = '7'
    confidence = '8'
    above = 'nn'
    below = 'mm'
    filttime1 = [55]
    filttime2 = [66]
    filtevent = ['uuu']
    filtip = ['cccc']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('business_table.html', business_data=testdata, config_data=configs, time1=filttime1,
                           time2=filttime2, events=filtevent, ips=filtip)


# 历史历史结果数据
@app.route('/history_result', methods=['POST', 'GET'])
def history_result():
    ip = []
    event = []
    business = []
    for i in range(0, 34):
        ip.append('20150322-20150333-' + str(i))
        event.append('20150333-20150344-' + str(i))
        business.append('20150355-20150366-' + str(i))
    testdata = [ip, event, business]
    return render_template('history_result.html', history_data=testdata)


# 删除历史结果数据
@app.route('/history_result_delete', methods=['POST', 'GET'])
def history_result_delete():
    row_event = request.form.get('rows_event')
    row_ip = request.form.get('rows_ip')
    row_business = request.form.get('rows_business')
    event_delete = []
    ip_delete = []
    business_delete = []
    event = []
    ip = []
    business = []
    for i in range(0, int(row_event)):
        if request.form.get('event' + str(i)):
            event_delete.append(request.form.get('event' + str(i)))
    for i in range(0, int(row_ip)):
        if request.form.get('ip' + str(i)):
            ip_delete.append(request.form.get('ip' + str(i)))
    for i in range(0, int(row_business)):
        if request.form.get('business' + str(i)):
            business_delete.append(request.form.get('business' + str(i)))
    for i in range(0, 12):
        ip.append('20150322-20150333-' + str(i))
        event.append('20150344-20150355-' + str(i))
        business.append('20150366-20150377-' + str(i))
    testdata = [ip, event, business]
    return render_template('history_result.html', history_data=testdata)


# 打开事件计算结果
@app.route('/history_result_event', methods=['POST', 'GET'])
def history_result_event():
    table_name = request.form.get('table_name');

    testdata = []
    for i in range(0, 15):
        testdata.append(['进行中', '201503' + str(i), '光纤交换机端口状态offline' + str(i), '10.6.1.1' + str(i), '几乎每天' + str(i),
                         '海航B2C' + str(i), 'S3' + str(i), 'VM11-TODE' + str(i), '1' + str(i), '3' + str(i),
                         '分析完毕' + str(i), '0' + str(i), '添加备注' + str(i), i])

    starttime = 'aaa'
    endtime = '456'
    compare = '7'
    confidence = '8'
    above = 'nn'
    below = 'mm'
    filttime1 = [11]
    filttime2 = [22]
    filtevent = ['sss']
    filtip = ['aaaa']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('event_result.html', event_result=testdata, config_data=configs, time1=filttime1,
                           time2=filttime2, events=filtevent, ips=filtip)


# 打开IP计算结果
@app.route('/history_result_ip', methods=['POST', 'GET'])
def history_result_ip():
    table_name = request.form.get('table_name');

    testdata = []
    for i in range(0, 16):
        testdata.append(['进行中', '201503' + str(i), '10.6.1.1' + str(i), '光纤交换机端口状态offline' + str(i), '几乎每天' + str(i),
                         '海航B2C' + str(i), 'S3' + str(i), 'VM11-TODE' + str(i), '1' + str(i), '3' + str(i),
                         '分析完毕' + str(i), '0' + str(i), '添加备注' + str(i), i])
    starttime = 'bbb'
    endtime = '456'
    compare = '7'
    confidence = '8'
    above = 'nn'
    below = 'mm'
    filttime1 = [33]
    filttime2 = [44]
    filtevent = ['ttt']
    filtip = ['bbbb']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('ip_result.html', ip_result=testdata, config_data=configs, time1=filttime1, time2=filttime2,
                           events=filtevent, ips=filtip)


# 打开业务计算结果
@app.route('/history_result_business', methods=['POST', 'GET'])
def history_result_business():
    table_name = request.form.get('table_name');

    testdata = []
    for i in range(0, 17):
        testdata.append(['进行中', '201503' + str(i), '海航B2C' + str(i), '光纤交换机端口状态offline' + str(i), '10.6.1.1' + str(i),
                         '几乎每天' + str(i), 'S3' + str(i), 'VM11-TODE' + str(i), '1' + str(i), '3' + str(i),
                         '分析完毕' + str(i), '0' + str(i), '添加备注' + str(i), i])

    starttime = 'xccc'
    endtime = '456'
    compare = '7'
    confidence = '8'
    above = 'nn'
    below = 'mm'
    filttime1 = [55]
    filttime2 = [66]
    filtevent = ['uuu']
    filtip = ['cccc']

    cache.set('startime', starttime, timeout=240 * 60)
    cache.set('endtime', endtime, timeout=240 * 60)
    cache.set('compare', compare, timeout=240 * 60)
    cache.set('confidence', confidence, timeout=240 * 60)
    cache.set('above', above, timeout=240 * 60)
    cache.set('below', below, timeout=240 * 60)
    cache.set('filttime1', filttime1, timeout=240 * 60)
    cache.set('filttime2', filttime2, timeout=240 * 60)
    cache.set('filtevent', filtevent, timeout=240 * 60)
    cache.set('filtip', filtip, timeout=240 * 60)

    configs = []
    configs.extend([starttime, endtime, compare, confidence, above, below])
    return render_template('business_result.html', business_result=testdata, config_data=configs, time1=filttime1,
                           time2=filttime2, events=filtevent, ips=filtip)


@app.route('/charts', methods=['POST', 'GET'])
def chart():
    if request.form.get('type') == 'everyday':
        data = {
            'name': ['2015-03-01', '2015-03-02', '2015-03-03', '2015-03-04', '2015-03-05', '2015-03-06', '2015-03-07'],
            'value': [269, 158, 215, 219, 216, 136, 139]}
    if request.form.get('type') == 'time':
        data = {'name': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                'value': [55, 19, 19, 9, 11, 16, 20, 41, 48, 105, 152, 94, 78, 81, 82, 80, 90, 95, 68, 40, 44, 35, 44,
                          26]}
    if request.form.get('type') == 'top_event':
    # 帕累托图
        data = Pareto(starttime,endtime)
    # 一线前十事件
    if request.form.get('type') == 'top_first':
        data = tongji1(starttime,endtime)
    # 二线前十事件
    if request.form.get('type') == 'top_second':
        data = tongji2(starttime,endtime)
    if request.form.get('type') == 'top_ip':
        data = {'name': ['10.6.137.109', '10.6.137.111', '10.6.137.108', '10.6.137.107', '10.6.137.105', '10.6.137.112',
                         '10.6.137.115', '10.6.137.189', '10.6.137.126', '10.6.137.121', ],
                'value': [64, 64, 63, 63, 61, 61, 59, 53, 45, 45]}
    # 前十业务
    if request.form.get('type') == 'top_business':
         data = tongjiB(starttime,endtime)
    # 核心业务
    if request.form.get('type') == 'chart_core':
        data = Core_Business(starttime,endtime)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
