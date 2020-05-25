# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 16:54:10 2019

@author: Administrator
"""
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
from flask import Flask,render_template,request
import valueYXB,json


app = Flask(__name__)
@app.route('/tx3',methods=['POST','GET'])
def query():
    note = '<b>评估须知：</b><P>⑴.英雄榜格式：http://bang.tx3.163.com/bang/role/xx_xxxxxx</br>角色名称格式：服务器+角色全名，需用-号分隔，比如“天下无双-壹枝穿云箭”<P>⑵.右上角+号可展开补充时装珍兽等信息，如不展开默认评估数据来源为英雄榜(主)+藏宝阁(辅)<P>⑶.调整因子是比较同门派同等级同价位的角色所得，如果为0表示可供比较的角色不足10人故不计，调整因子越全代表参考价值越高'
    note = note + '<p><b>更新日志：</b><P>2019-02-27 增加七曜星盘评估'
    select1 = 'selected="selected"'
    select2 = ''
    if request.method == "GET":
        return render_template('homePage.html',info=note,select1=select1,select2=select2)            
    elif request.method == 'POST':  
        if request.form['module'] == 'yxb':
            yxb = request.form['yxb']
        elif request.form['module'] == 'name':
            yxb = 'http://bang.tx3.163.com/bang/get_role?name='+request.form['yxb'].split('-')[1]+'&server='+request.form['yxb'].split('-')[0]          
            select1 = ''
            select2 = 'selected="selected"'
        #if re.match(r'http://bang.tx3.163.com/bang/role/\d{1,3}_\d{3,9}',yxb,flags=0) or re.match(r'[\u4e00-\u9fa5]{3,4}+{1}',yxb,flags=0):
        role_info = valueYXB.JueseGuzhi(yxb)
        showInfo = ''
        for x in role_info:
            if x in ['服务器','角色名称','门派','等级','神启境界','人物加护估值','人物炼护估值','孩子加护估值','人物装备估值','孩子装备估值','防护特技估值','元魂珠估值','孩子资质估值','孩子点化及天书估值','PVE等级估值','人物等级估值','修为调整因子','装评调整因子','攻击调整因子','防御调整因子','金色属性调整因子','评估区间','错误','山河画卷估值','门派及流派调整']:
                showInfo = showInfo + '<b>' + x + '</b>：'+role_info[x] + '<br>'
        #模板传参的方式很笨重，每个参数传一次，应该有更好的方法
        return render_template('homePage.html',info=showInfo,prompt=request.form['yxb'],align="text-align:center",select1=select1,select2=select2)
#        else:
#            return render_template('homePage.html',info=note) 
        
    
@app.route('/sendAjax',methods=['POST'])
def sendAjax():
    data = json.loads(request.form.get('data'))
    print(data)
    if data['module'] == 'yxb':
        yxb = data['role']
    elif data['module'] == 'name':
        yxb = 'http://bang.tx3.163.com/bang/get_role?name='+data['role'].split('-')[1]+'&server='+data['role'].split('-')[0]
    role_info = valueYXB.JueseGuzhi(yxb,data)
    print(role_info)
    for x in list(role_info.keys()):
        if x not in ['服务器','角色名称','门派','等级','神启境界','人物加护估值','人物炼护估值','孩子加护估值','人物装备估值','孩子装备估值','防护特技估值','特殊时装估值','珍兽估值','VIP估值','元魂珠估值','孩子资质及武学估值','孩子点化及天书估值','PVE等级估值','人物等级估值','修为调整因子','装评调整因子','攻击调整因子','防御调整因子','金色属性调整因子','评估区间','错误','山河画卷估值','灵兽乾元丹估值','灵兽七曜星盘估值','门派及流派调整','数据来源']:
            del(role_info[x])

    #return jsonify(role_info)   # 如果返回json对象，在前端会被自动排序，改为返回json字符串
    return json.dumps(role_info,ensure_ascii=False)

         
if __name__ == '__main__':
    app.debug = True
    app.config['JSON_AS_ASCII'] = False
    server = pywsgi.WSGIServer( ('localhost', 8888 ), app )
    server.serve_forever()
    #app.run(host='localhost',port=8888,debug=False,threaded = True)   #这里不能用localhost或者127.0.0.1,要用服务器的私有地址172.18.147.14