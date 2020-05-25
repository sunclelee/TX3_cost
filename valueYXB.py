# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 11:19:03 2019
重要函数：通过英雄榜评估角色价值
修改记录：
20190208 ⑴副本装的特技修改为不值钱 ⑵87风荷套修改为不值钱
20190217 发布2.0版本
20190218 ⑴解决时装珍兽如果人为输入空格会报错 
20190219 ⑴解决装备刻字"特技属性"导致特技统计报错
20190221 ⑴细化异常报错信息(缺少孩子,查无此人,孩子装备信息缺失等)
20190224 ⑴山河画卷评分减去400初始分再进行评估,完封从1800降到1500
20190225 ⑴最终估值钻钱保底 ⑵增加七曜星盘估值
20190227 ⑴修正软件估值总和最低为负的不合理之处 ⑵防御权重保底调为0.5 ⑶对装评大于130000的高端号,因为调整因子出不来,以装评增加一个系数
20190303 ⑴修正武器签名模拟太初星点图案,造成误判为太初的BUG
20190306 ⑴增加激活元魂珠的判断,如果没有4星珠激活,元魂珠估值根据钻数倒扣100-600不等
20190307 ⑴5星太初增值调整到6000,因为获取途径只有名人堂
20190312 ⑴增加炼护孔估值,主要是对拆钻号有用 ⑵修改主要孩子的判断,孩子加护默认+1
20190314 ⑴对误差较大的进行日志跟踪
20190315 ⑴对人物装备的加护和炼护,修改总数量评估为逐件评估,提高准确率
20190317 ⑴调整各项因子的权重,比较对象从以前的均值改为中高水平
20190318 ⑴调整因子不影响钻钱
@author: Administrator
"""

import requests,pymysql,datetime,re,traceback,json
from bs4 import BeautifulSoup
import function as fun

def GetZhuangbeiXinxi(equip_detail): #获取装备信息
    key = {}
    try:
        key['名称'] = equip_detail.select('.eq_type')[0].text
    except:
        raise RuntimeError('人物装备缺失')
    ttt = equip_detail.select('.tx3TextBlock')[0]['tx3text'].split('#')
    #print(equip_detail.select('.tx3TextBlock')[0]['tx3text'])
    if equip_detail.select('.tx3TextBlock')[0]['tx3text'][:100].count('#920') > 0 or equip_detail.select('.tx3TextBlock')[0]['tx3text'][:100].count('#921') > 0:  #只有太初有星级，只取前100个字符比较，避免玩家签名模拟星点误判
        key['星级'] = equip_detail.select('.tx3TextBlock')[0]['tx3text'][:100].count('#920') + equip_detail.select('.tx3TextBlock')[0]['tx3text'][:100].count('#921') 
    for i in range(0,len(ttt)):
        if '贵重等级' in ttt[i] and 'cCFB53B' not in ttt[i]:
            key['贵重等级'] = ttt[i].split('：')[1]
        elif '加护值' in ttt[i] and 'cCFB53B' not in ttt[i]:
            key['加护值'] = ttt[i].count('^')-ttt[i].count('^84')
        elif '炼护值' in ttt[i] and 'cCFB53B' not in ttt[i]:
            key['炼护值'] = ttt[i].count('^')-ttt[i].count('^93')-ttt[i].count('^92')
            key['炼护孔'] = ttt[i].count('^')
        elif '特技属性' in ttt[i] and 'cCFB53B' not in ttt[i] and 'cCFB53B' not in ttt[i-1]:  #cCFB53B是装备签名颜色，排除人为恶搞签名特技属性啥的
            if '(' in ttt[i].split('：')[1]:
                key['特技'] = ttt[i].split('：')[1][:ttt[i].split('：')[1].find('(')]
            else:
                key['特技'] = ttt[i].split('：')[1]
    return key   
  
def GetRenwuZhuangbei(info:list ,info2:list):  #人物装备估值
#    print(info)
    dengji = int(info2['等级'])
    shenqi = info2['神启境界']
    zuanGuzhi = int(info2['人物加护估值']) + int(info2['人物炼护估值'])
    def findName(xxx,name): #返回装备在XXX中的索引
        for i in xxx.keys():
            if name in xxx[i]:
                return i
                break        
    #xxx 每个值第一个元素表示装备等级，第二个元素表示满足条件的增值
    if dengji <=69:
        xxx = {0:[102,100,'帽子'],1:[102,100,'衣服'],2:[102,100,'腰带'],3:[102,100,'裤子'],4:[96,200,'门派特殊装备'],5:[95,150,'武器'],
               6:[91,80,'玉佩'],7:[92,100,'项链'],8:[102,100,'护肩'],9:[102,100,'护腕'],10:[102,100,'下摆'],11:[102,100,'靴子'],
               13:[108,100,'戒指'],14:[108,100,'戒指'],15:[91,50,'耳环'],16:[91,50,'耳环']} #17,18手镯没有金色装备不计
    elif dengji <=74:
        xxx = {0:[84,20,'帽子'],1:[84,20,'衣服'],2:[84,20,'腰带'],3:[84,20,'裤子'],4:[87,50,'门派特殊装备'],5:[100,250,'武器'],
               6:[96,100,'玉佩'],7:[98,120,'项链'],8:[84,20,'护肩'],9:[84,20,'护腕'],10:[84,20,'下摆'],11:[84,20,'靴子'],
               13:[96,100,'戒指'],14:[96,100,'戒指'],15:[96,70,'耳环'],16:[96,70,'耳环']} #17,18手镯没有金色装备不计
    elif dengji <=79:
        xxx = {0:[88,40,'帽子'],1:[88,40,'衣服'],2:[88,40,'腰带'],3:[88,40,'裤子'],4:[96,200,'门派特殊装备'],5:[108,400,'武器'],
               6:[110,200,'玉佩'],7:[110,200,'项链'],8:[88,40,'护肩'],9:[88,40,'护腕'],10:[88,40,'下摆'],11:[88,40,'靴子'],
               13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = {0:[92,70,'帽子'],1:[92,70,'衣服'],2:[92,70,'腰带'],3:[92,70,'裤子'],4:[96,200,'门派特殊装备'],5:[108,400,'武器'],
                   6:[110,200,'玉佩'],7:[110,250,'项链'],8:[92,70,'护肩'],9:[92,70,'护腕'],10:[92,70,'下摆'],11:[92,70,'靴子'],
                   13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
        else:
            xxx = {0:[97,100,'帽子'],1:[97,100,'衣服'],2:[97,100,'腰带'],3:[97,100,'裤子'],4:[96,200,'门派特殊装备'],5:[108,400,'武器'],
                   6:[110,200,'玉佩'],7:[110,250,'项链'],8:[97,100,'护肩'],9:[97,100,'护腕'],10:[97,100,'下摆'],11:[97,100,'靴子'],
                   13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
    result = 0
    for i in range(0,len(info)):
        if info[i]['名称'] in ['武器','针','剑','单刀','笔','长刀','双锤','弓箭','杖','双刀','巫杵','伞']: 
            if '星级' in info[i]:
                if info[i]['星级'] == 3:
                    result += 200
                elif info[i]['星级'] == 4:
                    result += 600
                elif info[i]['星级'] == 5:
                    result += 6000
            elif int(info[i]['贵重等级']) >= xxx[5][0]:
                result += xxx[5][1]
        elif info[i]['名称'] in ['帽子','衣服','腰带','裤子','门派特殊装备','玉佩','项链','护肩','护腕','下摆','靴子','戒指','耳环']:
            x = findName(xxx,info[i]['名称'])
            if int(info[i]['贵重等级']) >= xxx[x][0] and (int(info[i]['贵重等级']) not in [87,90]):  #风荷套是87套，贪痴套是90贵重但不值钱，这里会漏算74级的门派副手(87级)，50元无所谓了
                result += xxx[x][1]
            elif int(info[i]['贵重等级']) == 93 and x in [0,1,2,3,8,9,10,11]:  #天魂战场套在英雄榜上显示的贵重等级只有93，比地魂世界套还低，做一个特殊的处理
                result += 100
            elif int(info[i]['贵重等级']) == 108 and x == 7: #108级的项链也给点
                result += 150
            elif '天魂' in shenqi:
                if int(info[i]['贵重等级']) < 88: #对神启严格点，装备太差要扣
                    result -= 100
                elif int(info[i]['贵重等级']) in [92,96] and x in [0,1,2,3,8,9,10,11]: #地魂套还是适当给点，但价格贵了就要扣
                    if zuanGuzhi <= 1500:
                        result += 20
                    else:
                        result = result - min(200,int(80*zuanGuzhi/2300))
    return max(result,0)

def GetHaiziZhuangbei(info :list): ##孩子装备估值,同样的装备比人物略便宜点
    result = 0    
    for i in range(0,len(info)):
        if i == 0: # 武器
            if '星级' in info[i]:
                if info[i]['星级'] == 3:
                    result = result + 150
                elif info[i]['星级'] == 4:
                    result = result + 500
                elif info[i]['星级'] == 5:
                    result = result + 5000   
            elif int(info[i]['贵重等级']) >= 108:
                result = result + 300
        elif i in [1,2,3,4]: #铠甲
            try:
                if int(info[i]['贵重等级']) in [93,97]: #天魂套
                    result = result + 80
                elif int(info[i]['贵重等级']) in [92,96]: #地魂套
                    result = result + 50
            except:
                raise RuntimeError('孩子装备信息缺失')
        elif i == 5: #项链
            try:
                if int(info[i]['贵重等级']) >= 110:  #79级金色项链
                    result = result + 200
                elif int(info[i]['贵重等级']) == 108:  #78级金色项链
                    result = result + 100
            except:
                raise RuntimeError('孩子装备信息缺失')
    return result

def GetFlylv(shenqi): #把神启境界转为数字
    tran = {'壹' : '1', '贰' : '2', '叁' : '3', '肆' : '4', '伍' : '5', '陆' : '6', '柒' : '7', '捌' : '8', '玖' : '9'}
    if '魂' not in shenqi:
        return 0
    else:
        if '天' in shenqi:
            a = '2'
        elif '地' in shenqi:
            a = '1'
        b = tran[shenqi[2]]
        c = tran[shenqi[4]]
#        print(a + b + c)
        return int(a+b+c)

def PingguQujian(num): #把估值转为区间，低于1000区间幅度为200，高于1000幅度±10%递减，高于100000区间幅度为±5%
    num = round(int(num)/10,0)*10
    if num <= 1000:
        low = max(0,num - 100)
        high = max(200 - num,num + 100)
    elif num <= 100000:
        low = round(num*(0.9+num/100000*0.05)/10,0)*10
        high = round(num*(1.1-num/100000*0.05)/10,0)*10
    else:
        low = round(int(num*0.95)/10,0)*10
        high = round(int(num*1.05)/10,0)*10
    return str(low)+'-'+str(high)      
    
#------主函数------#    
def JueseGuzhi(url,data:dict):  #传入补充信息
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer' : 'https://tx3.cbg.163.com/cgi-bin/equipquery.py?act=show_overall_search'
        }
    #url= 'http://bang.tx3.163.com/bang/get_role?name=网瘾男神温言言&server=白云山' 
    req = requests.get(url,headers = header)
    if req.status_code == 200:
        html = req.text
        soup = BeautifulSoup(html,'lxml')
        conn = pymysql.connect(host='localhost',port=3306,user='root',password='yhwj1234',db='zhilianzhaopin',charset='utf8')
        #判断主娃，获取孩子装备
        try:
            try:
                dengji = soup.select('.dInfo .dInfo_1 .sLev')[0].select('em')[1].text
            except:
                raise RuntimeError('查无此号')
            fuwuqi = soup.select('.dInfo .dInfo_1 .sExp')[1].select('a')[0].text.split('\xa0')[1]
            roleName = soup.select('.dInfo .dInfo_1 .sTitle')[0].text
            ##此处获取英雄榜没有的信息
            if data['isExtra'] == True: #前端选择了补充信息
                if data['clothesNum'].strip() == '':
                    clothesNum = 0
                else:
                    clothesNum = data['clothesNum']
                #获取时装列表
                specialClothes = []
                for x in data['clothesList']:
                    for y in fun.clothes:
                        if int(x) in fun.clothes[y]:
                            specialClothes.append(y)
                            
                if data['riderNum'].strip() == '':
                    riderNum = 0
                else:
                    riderNum = data['riderNum']
                #获取珍兽列表
                specialRiders = []
                for x in data['riders']:
                    for y in fun.riders:
                        if int(x) in fun.riders[y]:
                            specialRiders.append(y)
                #获取VIP
                if data['vip'] == '9':
                    VIP9 = '是'
                else:
                    VIP9 = '否' 
                #获取地魂合体元魂珠个数
                dihunNum = data['yuanhunzhu']
                dataFrom = '英雄榜和人为补充'
                jishouJiage = '未知'
            else: #前端未选择补充信息#去数据库找找
                cursor = conn.cursor()
                if cursor.execute("SELECT 价格,天地魂合体珠,VIP9,特殊时装,特殊珍兽,珍兽数量 FROM tx3 WHERE 角色名称='"+roleName+"' AND 服务器='"+fuwuqi+"' AND 等级="+dengji+" AND 更新时间>=DATE_SUB(CURDATE(),INTERVAL 30 DAY) ORDER BY 更新时间 DESC"):
                    j = cursor.fetchone()
                    dbInfo = {}
                    for i in range(0,len(cursor.description)):
                        dbInfo[cursor.description[i][0]] = j[i] 
                    clothesNum = ''
                    specialClothes = dbInfo['特殊时装'].split('|')
                    if dbInfo['珍兽数量'] == None:
                        riderNum = 0
                    else:
                        riderNum = dbInfo['珍兽数量']
                    if dbInfo['特殊珍兽'] == None:   #有部分账号特殊珍兽为None,None没有split方法，需转换为''
                        dbInfo['特殊珍兽'] = ''
                    specialRiders = dbInfo['特殊珍兽'].split('|')
                    VIP9 = dbInfo['VIP9']
                    if dbInfo['天地魂合体珠'] == '':
                        dihunNum = 0
                    else:
                        dihunNum = len(dbInfo['天地魂合体珠'].split('|'))
                    dataFrom = '英雄榜和藏宝阁'
                    jishouJiage = dbInfo['价格']
                else:
                    clothesNum = 0
                    specialClothes = []
                    riderNum = 0
                    specialRiders = []
                    VIP9 = '未知'
                    dihunNum = 0
                    dataFrom = '英雄榜'
                    jishouJiage = '未知'
                cursor.close
            childShuxing = soup.select('#tableCHILD .TableContent.TableContents_2')
            bbb = []
            for x in range(0,len(childShuxing)):
                #英雄榜上没有孩子名气，估算为(资质/1000+武学/10+1)×(孩子加护+1)，值最大的就是主娃
                mingqi = round((float(childShuxing[x].select('.li2')[1].text)/1000 + float(childShuxing[x].select('.li3')[2].text)/10 + 1)*(float(childShuxing[x].select('.li2')[4].text)+1),2) 
                bbb.append(mingqi)
            try:
                zhuWa = bbb.index(max(bbb)) 
            except:
                raise RuntimeError('没有孩子信息')
            #获取孩子装备
            haiziZhuangbei = []
            childZhuangbei = soup.select('#tableCHILD .TableContent.TableContents_1')[zhuWa].select('.equip_pic')
            for i in range(0,len(childZhuangbei)):
                haiziZhuangbeiDetail = {}
                haiziZhuangbeiDetail['名称'] = childZhuangbei[i]['title_name'][8:]
                zzz = childZhuangbei[i]['intro'].split('#')
                if childZhuangbei[i]['intro'].count('#920') > 0 or childZhuangbei[i]['intro'].count('#921') > 0:
                    haiziZhuangbeiDetail['星级'] = childZhuangbei[i]['intro'].count('#920') + childZhuangbei[i]['intro'].count('#921')
                for j in zzz:
                    if '贵重等级' in j:
                        haiziZhuangbeiDetail['贵重等级'] = j.split('：')[1]
                    elif '点化' in j:
                        haiziZhuangbeiDetail['点化条数'] = childZhuangbei[i]['intro'][childZhuangbei[i]['intro'].find('点化'):].count('c84D2DB')
                haiziZhuangbei.append(haiziZhuangbeiDetail)   
            #点化估值
            dianhua = 0
            for i in haiziZhuangbei:
                if '点化条数' in i:
                    if i['点化条数'] == 3:
                        dianhua = dianhua + 60
                    elif i['点化条数'] == 4:
                        dianhua = dianhua + 200
                    elif i['点化条数'] >= 5:
                        dianhua = dianhua + 3000
            #天书估值
            tianshu = 0
            for x in soup.select('.tianshu-img-list.clear'):
                if x.select('li'):
                    for i in x.select('li'):
                        for j in i['intro'].split('#'):
                            if '尚书令等级' in j:
                                if int(re.sub("\D","",j)) >= 2:
                                    tianshu = tianshu + 80*pow(2,int(re.sub("\D","",j))-2)
                                mmm = i['intro'][i['intro'].find('尚书令等级'):].count('#r#c') #评估天书条数
                                if mmm == 2:
                                    tianshu = tianshu + 50
                                elif mmm == 3:
                                    tianshu = tianshu + 120
                                elif mmm >= 4:
                                    tianshu = tianshu + 400

            #获取元魂珠
            YHZlist = []
            yuanHunZhu = soup.select('#tableYHZ .LeftSideNav')[0].select('li')
            for x in range(0,len(yuanHunZhu)):
                YHZlist.append(yuanHunZhu[x].text)
            #元魂珠估值，注意跟等级和专服有关，因为不能显示技能树，所以无法判断是否开有天地魂，如果是6星珠默认开启天地魂
            if int(dengji) <= 69:
                yuanhunzhuShuxingdian = [1400,1600,1800]  #各星级元魂珠价值的最低属性点
            elif int(dengji) <= 74:
                yuanhunzhuShuxingdian = [1450,1700,1900]
            else:
                yuanhunzhuShuxingdian = [1600,1780,1950]
            yuanhunzhuValue = 0
            jihuozhu = False
            #print(YHZlist)
            for i in range(0,len(YHZlist)):
                #print(YHZlist[i])
                if YHZlist[i] == '喜气洋羊':
                    yuanhunzhuValue += 600
                    if fuwuqi == '飞鸿踏雪':   #79专服年兽珠子更贵一些
                       yuanhunzhuValue += 200 
                elif YHZlist[i] == '显圣真君':
                    yuanhunzhuValue += 400
                    if fuwuqi == '飞鸿踏雪':
                       yuanhunzhuValue += 200 
                elif YHZlist[i] in ['马王爷元魂珠','广寒仙子']:
                    yuanhunzhuValue += 200
                    if fuwuqi == '飞鸿踏雪':
                       yuanhunzhuValue += 100 
                elif YHZlist[i] in ['昴日星官','八杀骑劫','万圣天尊','业火元魂珠']:
                    yuanhunzhuValue += 100 
                elif YHZlist[i] not in ['霸王元魂珠'] and '残魂' not in YHZlist[i] and int(soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].select('.li1')[1].text) >= 4:
                    jihuozhu = True
                    chengzhang = round(float(soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].find('li',text='成长优势：').findNext('li').text),0)
                    xibie = soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].find('li',text='系别：').findNext('li').text                      
                    eee = soup.select('#tableYHZ .TableContents_2')[i].find('p',text='基本属性').findNext('ul')
                    maxQianneng = max(float(eee.select('.li3.len-li3')[0].text),float(eee.select('.li3.len-li3')[1].text),float(eee.select('.li3.len-li3')[2].text),float(eee.select('.li3.len-li3')[3].text),float(eee.select('.li3.len-li3')[4].text),float(eee.select('.li3.len-li3')[5].text))        
                    if int(soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].select('.li1')[1].text) == 4:
                        if xibie == '水生系': #4星魚很受欢迎可以算高点
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[0]+250)))
                        else:
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[0])))
                    elif int(soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].select('.li1')[1].text) == 5:
                        if xibie == '水生系':
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[1]+100)))   
                        else:
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[1])))                  
                    elif int(soup.select('#tableYHZ .TableContents_1 .DataListStyle')[i].select('.li1')[1].text) >= 6:
                        if xibie == '水生系':
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[2]+100))) + 100
                        else:
                            yuanhunzhuValue += int(max(1-(1300-chengzhang)/20,0)*(max(0,int(maxQianneng)-yuanhunzhuShuxingdian[2]))) + 100 #6星珠不容易，多加100               
                    #print(xibie,chengzhang,maxQianneng)
            yuanhunzhuValue += 200*int(dihunNum)   #地魂合体算200/个                                 
            #获取人物装备信息
            renwuZhuangbei = []
            for i in range(0,len(soup.select('.detail_wrap_block'))):
                if '山河画卷' not in soup.select('.detail_wrap_block')[i].text: #山河图与装备的关键字不同，单独分析
                    xxx = soup.select('.detail_wrap_block')[i]
                    renwuZhuangbei.append(GetZhuangbeiXinxi(xxx))
            shanheHuajuan = fun.GetShanhe(soup)   #h获取山河画卷          
            #获取人物加护和炼护 ，以及炼护孔估值
            jiahu,lianhu,lianhukongValue,jiahuValue,lianhuValue = 0,0,0,0,0
            for i in range(0,len(renwuZhuangbei)):
                if '加护值' in renwuZhuangbei[i]: 
                    jiahu += renwuZhuangbei[i]['加护值']
                    jiahuValue += fun.GetJiahuValue(fun.jiahuScore,renwuZhuangbei[i]['加护值']*18)/18 #逐件计算加护值
                if '炼护值' in renwuZhuangbei[i]:
                    lianhu += renwuZhuangbei[i]['炼护值']   
                    lianhuValue += fun.GetJiahuValue(fun.lianhuScore,renwuZhuangbei[i]['炼护值']*15)/15
                if '炼护孔' in renwuZhuangbei[i]:
                    lianhukongValue += fun.GetliankongValue(str(renwuZhuangbei[i]['炼护值']),str(renwuZhuangbei[i]['炼护孔']))
            print('炼护孔价值%s'%lianhukongValue)
     
            #获取防护特技
            equipSkill = []
            huXin,huoyuanFanghu,dunciFanghu,huikanFanghu,fengshuiduFanghu,quxiSanhui = 0,0,0,0,0,0
            if soup.find(title_name='#c00C0FF无懈·完封'):
                wanFeng = int(re.sub("\D","",soup.find(title_name='#c00C0FF无懈·完封').text))  #获取觉醒完封
            else:
                wanFeng = 0
            for i in range(0,len(renwuZhuangbei)):  # 防护特技不看铠甲，防止带特技的低阶装备误算;贵重81、82的不看，因为有部分副本装带特技
                if '特技' in renwuZhuangbei[i] and (renwuZhuangbei[i]['名称'] not in ['帽子','护肩','衣服','护腕','腰带','下摆','裤子','靴子']): 
                    if not ('贵重等级' in renwuZhuangbei[i] and renwuZhuangbei[i]['贵重等级'] in ['81','82']):
                        if '护心' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            huXin = huXin + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '火元防护' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            huoyuanFanghu = huoyuanFanghu + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '钝刺防护' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            dunciFanghu = dunciFanghu + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '挥砍防护' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            huikanFanghu = huikanFanghu + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '水风毒防护' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            fengshuiduFanghu = fengshuiduFanghu + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '驱邪散秽' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            quxiSanhui = quxiSanhui + int(renwuZhuangbei[i]['特技'].split('+')[1])
                        elif '完封' in renwuZhuangbei[i]['特技'].split('+')[0]:
                            wanFeng = wanFeng + int(renwuZhuangbei[i]['特技'].split('+')[1])    
            if huXin >= 10:
                equipSkill.append('护心')        
            if wanFeng >= 10:
                equipSkill.append('完封')
            if huoyuanFanghu >=10:
                equipSkill.append('火元防护')
            if dunciFanghu >=10:
                equipSkill.append('钝刺防护')
            if huikanFanghu >=10:
                equipSkill.append('挥砍防护')
            if fengshuiduFanghu >=10:
                equipSkill.append('水风毒防护')
            if ('火元防护' in equipSkill) and ('水风毒防护' in equipSkill):
                equipSkill.append('法术防护')
            if ('钝刺防护' in equipSkill) and ('挥砍防护' in equipSkill):
                equipSkill.append('物理防护')
            if ('物理防护' in equipSkill) and ('法术防护' in equipSkill):
                equipSkill.append('伤害防护')
            if quxiSanhui >=10:
                equipSkill.append('驱邪散秽') 
            
            #获取紫色的灵兽七曜星盘,灵兽通常不只一匹，遍历获取
            qiyaoXingpanToal = []
            for x in soup.select('#tableLS')[0].select('.TableContents'):
                Xingpan = []
                for y in ['#cBB44BB太阳','#cBB44BB太阴','#cBB44BB晨星','#cBB44BB太白','#cBB44BB荧惑','#cBB44BB岁星','#cBB44BB镇星']:
                    if x.find(tooltip_title=y):
                        xingdianDengji = x.find(tooltip_title=y)['tooltip_intro'].split('#r')[2].split('：')[1]
                        gaoHeJiu = str(x.find(tooltip_title=y)['tooltip_intro'].count('(中)'))+str(x.find(tooltip_title=y)['tooltip_intro'].count('(高)'))+str(x.find(tooltip_title=y)['tooltip_intro'].count('(究)'))
                        Xingpan.append(y[-2:]+str(xingdianDengji)+'-'+gaoHeJiu)                        
                if len(Xingpan)>=5: #至少满足5个星点才算钱
                    qiyaoXingpanToal.extend(Xingpan)
            
            #构建角色字典
            info = {}
            info['服务器'] = fuwuqi
            info['角色名称'] = roleName 
            info['门派'] = soup.select('.dInfo .dInfo_1 .sExp')[0].select('a')[0].text[0:2] 
            info['等级'] = dengji
            info['神启境界'] = soup.select('.dEquip.dEquip_2 .ulList_3 .ulList_3_v')[4].text + soup.select('.dEquip.dEquip_2 .ulList_3 .ulList_3_v')[5].text
            info['修为'] = soup.select('.dEquip.dEquip_2 .ulList_3 .ulList_3_v')[0].text
            info['装评'] = soup.select('.ulList_3 .ulList_3_v')[0].text
            info['加护'] = str(jiahu)
            info['炼护'] = str(lianhu)
            info['生命'] = soup.select('.ulList_4 .li_1')[0].text
            info['物防'] = re.sub("\D", "",soup.select('.ulList_6.ulList_h')[0].select('li')[1].text)
            info['法防'] = re.sub("\D", "",soup.select('.ulList_6.ulList_h')[0].select('li')[3].text)
            info['知彼'] = re.sub("\D", "",soup.select('.ulList_6.ulList_h')[0].select('li')[6].text)
            info['回避'] = re.sub("\D", "",soup.select('.ulList_6.ulList_h')[0].select('li')[2].text)
            info['神明'] = re.sub("\D", "",soup.select('.ulList_6.ulList_h')[0].select('li')[4].text)
            info['最大物攻'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[1].text.split('-')[1])
            info['最大法攻'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[3].text.split('-')[1])
            info['最小物攻'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[1].text.split('-')[0])
            info['最小法攻'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[3].text.split('-')[0])
            info['附伤'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[6].text)
            info['命中'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[2].text) 
            info['会心'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[5].text)
            info['重击'] = re.sub("\D", "",soup.select('.ulList_5.ulList_h')[0].select('li')[4].text)
            info['追电'] = re.sub("\D", "", soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_6')[1].select('li')[1].text)
            info['骤雨'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_6')[1].select('li')[2].text)
            info['疾语'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_6')[1].select('li')[3].text)
            info['人祸'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_6')[1].select('li')[6].text)
            info['万钧'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_5')[1].select('li')[6].text)
            info['铁壁'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_5')[1].select('li')[7].text)
            info['诛心'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_5')[1].select('li')[4].text)
            info['御心'] = re.sub("\D","",soup.select('.dEquip.dEquip_2 .dEquips_1 .ulList_5')[1].select('li')[5].text)  
            info['山河画卷'] = '|'.join(shanheHuajuan)
            info['七曜星盘'] = '|'.join(qiyaoXingpanToal)
            info['启慧等级'] = soup.select('.dEquip.dEquip_2 .ulList_3 .ulList_3_v')[6].text
            info['天灵点数'] = soup.select('.dEquip.dEquip_2 .ulList_3 .ulList_3_v')[7].text
            info['元魂珠'] = "|".join(YHZlist)
            info['孩子资质'] = childShuxing[zhuWa].select('.li2')[1].text
            info['孩子武学'] = childShuxing[zhuWa].select('.li3')[2].text
            info['孩子加护'] = re.sub("\D","",childShuxing[zhuWa].select('.li2')[4].text)
            info['VIP9'] = VIP9
            info['防护特技'] = '|'.join(equipSkill)
            info['特殊时装'] = '|'.join(specialClothes)
            info['特殊珍兽'] = '|'.join(specialRiders)
            info['珍兽数量'] = str(riderNum)
            info['查询时间'] = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
            info['英雄榜链接'] = req.url
            info['人物加护估值'] = str(int(jiahuValue))
            info['人物炼护估值'] = str(int(lianhuValue+lianhukongValue))
            info['孩子加护估值'] = str(int(fun.GetJiahuValue(fun.jiahuScore,int(info['孩子加护'])*3)/3))
            info['人物装备估值'] = str(GetRenwuZhuangbei(renwuZhuangbei,info))
            info['孩子装备估值'] = str(GetHaiziZhuangbei(haiziZhuangbei))
            info['防护特技估值'] = str(fun.GetTejiValue(info))
            info['特殊时装估值'] = str(int(fun.GetShizhuangValue(info['特殊时装'],clothesNum)*float(data['softvalue'])))  #软件价值根据前端的选择进行折算
            info['珍兽估值'] = str(int(fun.GetZhenshouValue(info['特殊珍兽'],riderNum)*float(data['softvalue']))) #软件价值根据前端的选择进行折算
            info['VIP估值'] = str(fun.GetVipValue(info))
            if int(info['VIP估值']) >= 0:
                info['VIP估值'] = str(int(int(info['VIP估值'])*float(data['softvalue'])))
            info['元魂珠估值'] = str(yuanhunzhuValue)
            if jihuozhu == False: #如果没有激活和合体珠子，根据钻的数量倒扣部分
                info['元魂珠估值'] = str(int(info['元魂珠估值']) - max(100,(int(info['加护'])+int(info['炼护'])-234-195)*10))
            info['孩子资质及武学估值'] = str(fun.GetHaiziValue(info))
            info['孩子点化及天书估值'] = str(dianhua + tianshu)
            info['PVE等级估值'] = str(int(fun.GetPveValue(info['启慧等级'],info['天灵点数'],info['等级'])*float(data['softvalue']))) #软件价值根据前端的选择进行折算
            info['人物等级估值'] = str(int(fun.GetDengjiValue(info,GetFlylv(info['神启境界']))))
            if int(info['人物等级估值']) >= 0:
                info['人物等级估值'] = str(int(int(info['人物等级估值'])*float(data['softvalue']))) #如果人物等级估值为正值根据前端的选择进行折算，为负不变因为是硬伤
            info['山河画卷估值'] = str(fun.GetHuajuan(shanheHuajuan))
            info['灵兽乾元丹估值'] = str(fun.GetMadanValue(soup))
            info['灵兽七曜星盘估值'] = str(fun.GetQiyaoxingpanValue(qiyaoXingpanToal))
            if '地魂' in info['神启境界']: #地魂没开战场，除了钻钱，其余估值打个7折
                info['硬件估值总和'] = str(int(max(0,int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])+ 0.7*(int(info['防护特技估值']) +int(info['孩子资质及武学估值']) + int(info['孩子点化及天书估值']) + int(info['人物装备估值']) + int(info['孩子装备估值'])+int(info['山河画卷估值'])+int(info['灵兽乾元丹估值'])+int(info['灵兽七曜星盘估值'])))))
                info['软件估值总和'] = str(int(0.7*(int(info['特殊时装估值']) + int(info['珍兽估值']) + int(info['VIP估值']) + int(info['元魂珠估值']) + int(info['PVE等级估值']) +int(info['人物等级估值']))))
            else:
                info['硬件估值总和'] = str(max(0,int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])+ int(info['防护特技估值']) + int(info['孩子资质及武学估值']) + int(info['孩子点化及天书估值']) + int(info['人物装备估值']) + int(info['孩子装备估值'])+int(info['山河画卷估值'])+int(info['灵兽乾元丹估值'])+int(info['灵兽七曜星盘估值'])))
                info['软件估值总和'] = str(int(info['特殊时装估值']) + int(info['珍兽估值']) + int(info['VIP估值']) + int(info['元魂珠估值']) + int(info['PVE等级估值']) +int(info['人物等级估值']))
            info['攻击期望'] = str(fun.GetGongjiQiwang(info,'fromYXB'))
            info['综合防御'] = str(fun.GetFangyu(info,'fromYXB'))
            info['金色属性'] = str(fun.GetJinseShuxing(info))
            info['流派'] = str(fun.GetLiupai(info))
            #以下info需链接数据库才能获取
            info['修为调整因子'] = str(fun.XiuweiTiaozheng(conn,info))
            info['装评调整因子'] = str(fun.ZhuangpingTiaozheng(conn,info))
            info['门派调整因子'] = str(fun.MengpaiTiaozheng(conn,info))
            info['攻击调整因子'] = str(fun.GongjiTiaozheng(conn,info))
            info['防御调整因子'] = str(fun.FangyuTiaozheng(conn,info))
            info['金色属性调整因子'] = str(fun.JinseTiaozheng(conn,info))    
            info['门派及流派调整'] = str(fun.LiupaiTiaozheng(conn,info))
            #拆钻对装评、攻击、防御影响很大,衰减这三个因子的权重
            chaizuan = 0.4+0.6*min(1,int(info['加护'])/234)
            #攻/受/中庸的攻击和防御权重略有不同
            ccc = float(info['综合防御'])/float(info['攻击期望'])
            if ccc >= 8: 
                gongjiQuanzhong = 2-min(ccc/8,1.9)  #越受的角色,攻击权重就越低,CCC超过15.2就认为攻击不重要了,权重仅为0.1
                fangyuQuanzhong = min(2,round(ccc/8,2)) #越受的角色，防御权重就越高，2封顶
            elif ccc>=5:
                gongjiQuanzhong = 1
                fangyuQuanzhong = 1
            else:   
                gongjiQuanzhong = 1.0
                fangyuQuanzhong = max(0.5,ccc/5)  #越攻的角色,防御权重就越低,但还是有0.5作为保底,因为受可以完全不要攻属性,但攻不能完全不要防御属性                         
            TiaozhengYinzi1 = 0
            for ab,quanZhong,item in [[info['攻击调整因子'],gongjiQuanzhong*chaizuan,'攻击调整因子'],[info['防御调整因子'],fangyuQuanzhong*chaizuan,'防御调整因子'],[info['金色属性调整因子'],0.6,'金色属性调整因子']]:
                if float(ab) != 0:
                    info[item] = str(round(max(-0.2,(float(ab)-1)*quanZhong)+1,3))  #属性调整因子最低0.8
                    TiaozhengYinzi1 = TiaozhengYinzi1 + max(-0.2,(float(ab)-1)*quanZhong)
            TiaozhengYinzi2 = 0
            for cd,quanZhong,item in [[info['修为调整因子'],0.5,'修为调整因子'],[info['装评调整因子'],0.6*chaizuan,'装评调整因子'],[info['门派及流派调整'],0.8,'门派及流派调整']]:
                if float(cd) != 0:
                    info[item] = str(round((float(cd)-1)*quanZhong+1,3))
                    TiaozhengYinzi2 = TiaozhengYinzi2 + (float(cd)-1)*quanZhong
            #最终估值=(硬件估值×(攻击调整+防御调整+金色调整)+软件估值)×(装评调整+修为调整+流派调整)  钻钱保底
            #info['最终估值'] = str(max(int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值']),int((int(info['硬件估值总和'])*(1+TiaozhengYinzi1)+int(info['软件估值总和']))*(1+TiaozhengYinzi2))))
            #最终估值=(钻钱+(硬件估值-钻钱)*(攻击调整+防御调整+金色调整)+软件估值)×(装评调整+修为调整+流派调整)
            zuanqian = int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])
            info['最终估值'] = str(max(zuanqian,int((zuanqian + (int(info['硬件估值总和'])-zuanqian)*(1+TiaozhengYinzi1)+int(info['软件估值总和']))*(1+TiaozhengYinzi2))))
            ##因为对高端号评估有点不完整，如果装评大于130000，调整因子没有出来就加点比例,比例方式为(装评-130000)/100000*2+1
            if [info['修为调整因子'],info['装评调整因子'],info['攻击调整因子'],info['防御调整因子'],info['金色属性调整因子'],info['门派及流派调整']].count('0') >= 2 and int(info['装评']) >= 130000:
                info['最终估值'] = int(int(info['最终估值'])*((int(info['装评'])-130000)/100000*2+1))
            info['市场调整金额'] = str(fun.ShichangTiaozheng(conn,info))
            #市场调整金额绝大部分都是正值，似乎没起到调节的作用，可能是CBG挂的价都偏高
            #评估区间以钻钱为下限
            info['评估区间'] = PingguQujian(int(info['最终估值'])) 
            info['数据来源'] = dataFrom
            info['寄售价格'] = str(jishouJiage)
            #print(info)
            ###写入数据库
            # cursor = conn.cursor()
            # if cursor.execute("SELECT * FROM tx3_yxb WHERE 角色名称='"+info['角色名称']+"' AND 服务器='"+info['服务器']+"' AND 查询时间>=DATE_SUB(CURDATE(),INTERVAL 1 DAY)"):
                # #如果角色的查询记录在当天已经存在，则更新该条记录的信息
                # sql3 = 'UPDATE tx3_yxb SET '
                # for x in info:
                    # sql3 = sql3 + x + "='" + info[x] + "',"
                # sql3 = sql3[:-1] + " WHERE 角色名称='"+info['角色名称']+"' AND 服务器='"+info['服务器']+"' AND 查询时间>=DATE_SUB(CURDATE(),INTERVAL 1 DAY)" 
                # cursor.execute(sql3)               
                # #cursor.execute("UPDATE tx3 SET 价格="+info['价格']+",更新时间='"+info['更新时间']+"',修为调整因子="+info['修为调整因子']+",装评调整因子="+info['装评调整因子']+",门派调整因子="+info['门派调整因子']+",特殊属性调整因子="+info['特殊属性调整因子']+",最终估值="+info['最终估值']+" WHERE 藏宝阁编号="+info['藏宝阁编号']+" AND 服务器='"+info['服务器']+"'")   
                # #cursor.execute("UPDATE tx3 SET 价格=%s,更新时间=%s,修为调整因子=%s,装评调整因子=%s,门派调整因子=%s,最终估值=%s WHERE 藏宝阁编号=%s AND 服务器=%s",(info['价格'],info['更新时间'],info['修为调整因子'],info['装评调整因子'],info['门派调整因子'],info['最终估值'],info['藏宝阁编号'],info['服务器']))
            # else:
                # sql1 = ",".join(info.keys())
                # sql2 = ""
                # for x in info:
                    # sql2 = sql2 + "'" + info[x] + "',"
                # #cursor.execute("INSERT INTO tx3(藏宝阁编号,服务器,角色名称,门派,性别,等级,神启境界,修为,装评,加护,炼护,价格,生命,物防,法防,知彼,回避,神明,最大物攻,最大法攻,最小物攻,最小法攻,附伤,命中,会心,重击,追电,骤雨,疾语,人祸,万钧,铁壁,诛心,御心,王朝军资,天域声望,启慧等级,天灵点数,特殊元魂珠,孩子资质,VIP9,防护特技,特殊时装)VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}','{37}','{38}','{39}','{40}','{41}','{42}');".format(info['藏宝阁编号'],info['服务器'],info['角色名称'],info['门派'],info['性别'],info['等级'],info['神启境界'],info['修为'],info['装评'],info['加护'],info['炼护'],info['价格'],info['生命'],info['物防'],info['法防'],info['知彼'],info['回避'],info['神明'],info['最大物攻'],info['最大法攻'],info['最小物攻'],info['最小法攻'],info['附伤'],info['命中'],info['会心'],info['重击'],info['追电'],info['骤雨'],info['疾语'],info['人祸'],info['万钧'],info['铁壁'],info['诛心'],info['御心'],info['王朝军资'],info['天域声望'],info['启慧等级'],info['天灵点数'],info['特殊元魂珠'],info['孩子资质'],info['VIP9'],info['防护特技'],info['特殊时装']))
                # #上面的execute也可以正常执行，但是太长了而且不易于维护，简化一下
                # #print("INSERT INTO tx3("+sql1+") VALUES("+sql2[:-1]+")")
                # cursor.execute("INSERT INTO tx3_yxb("+sql1+") VALUES("+sql2[:-1]+")")
            # conn.commit()  #commit可以放在这里提交整页数据，而不必每个角色提交一次
            # cursor.close()
            conn.close() 
            ##对评估不合理的角色进行日志跟踪
            tiaozhengJJJ = float(info['修为调整因子'])*float(info['装评调整因子'])*float(info['攻击调整因子'])*float(info['防御调整因子'])*float(info['金色属性调整因子'])*float(info['门派及流派调整'])
            if (info['寄售价格'] != '未知') and tiaozhengJJJ!=0 and (int(info['寄售价格'])/int(info['最终估值'])>1.15 or int(info['寄售价格'])/int(info['最终估值'])<0.85):           
                log = fun.Logger('误差.log',level='debug')
                log.logger.info(json.dumps(info,ensure_ascii=False))
        except Exception as e:
            traceback.print_exc()  #抛出带行数的错误信息
            conn.close()
            info = {}
            if e.args[0] in ['没有孩子信息','查无此号','孩子装备信息缺失','人物装备缺失']:
                info['错误'] = e.args[0]
            else:
                info['错误'] = '英雄榜信息缺失'           
        return info
        
print(JueseGuzhi('http://bang.tx3.163.com/bang/role/27_3637069',{'isExtra':False,'softvalue':'1'}))  