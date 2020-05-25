# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 09:55:53 2018
修改记录：
20190208 ⑴修改GetFangyu函数，对于天机，英雄榜的防御要还原成真实防御，因为英雄榜有玄修加成
20190211 ⑴74级的等级钱修改为90,79的等级钱修改为150,天魂6天适当提高200 ⑵降低雷钻的价值，234钻从1500降到1300
20190218 ⑴调整部分特技估值,主要是单防护特技价值降低 ⑵调整物理幽簧算攻击期望的时候附伤所占权重从0.5到1 ⑶增加幽都月明时装
20190219 ⑴修改修为装评攻击防御金色属性等调整因子找同价位号为寄售价格（3月上线，因为价格有很多虚高，不能真实反映市场）
20190225 ⑴调整人物等级估值,从最多扣400调为最多扣1200 ⑵调整部分炼护钻钱,主要是增高
20190226 ⑴调整个别人物等级估值
20190228 ⑴调整七曜星盘的估值,打6折,因为材料贬值了
20190302 ⑴GetRenwuZhuangbei函数针对天魂角色穿地魂套,根据加护值扣掉响应估值
20190305 ⑴流派调整因子增加一个搜索条件"价格<1.5*最终估值",剔除挂高了的价格
20190306 ⑴对小攻羽毛,因为有玄修加成,所以英雄榜的攻击降低20%再与藏宝阁数据做比较
20190307 ⑴5星太初增值调整到6000,因为获取途径只有名人堂
20190312 ⑴调整山河画卷估值函数,对于估值为0但是强化大于30%,纯靠等级冲上去的画卷,适当给100-400
20190313 ⑴取消鹰击长空的特殊时装资格
20190314 ⑴孩子武学的评估与孩子装备和孩子加护的价值关联,孩子必须高富帅才对得起高武学的评估 ⑵加入日志记录误差较大的角色
20190317 ⑴调整各项因子的权重,比较对象从以前的均值改为中高水平
20190319 ⑴对综合防御的计算,调整了知彼的影响方式,知彼对血量直接影响,更加合理,也增加了血量的比重,从以前/4改为/2
20190321 ⑴修正logging重复记录日志的问题
@author: Administrator
"""
#----------时装函数-----------#
import re
global clothes,mengPai,rider
clothes = {
            '海棠未雨' : [121705,121706,210037,210038,210039,210040,210073,210074],
            '沧海桑田' : [210000,210001,210002,210003,210004,210005],
            '天狐霓裳' : [210148,210149,210210,210211],
            '绛云思暖' : [21339,21340,121531,121532],
            '蟾宫折桂' : [21487,21488,121515,121516,121580,121581],
            '凤羽紫凰' : [21399,21400,88331,88332],
            '剑影流枫' : [210204,210205,210290,210291],
            '心之所属' : [121634,121635],
            '黛染青花' : [21189,21190,21202,21203,121533,121534,121572,121573],
            #'鹰击长空' : [21449,21450],
            '疏影横斜' : [121745,121746,121747,121748,121749,121750,121751,121752],
            '祈福同心' : [21059],
            '孤鸿月影' : [21293,21294,21323,21324,121576,121577],
            '大圣金甲' : [121661,121662,121663,121664],
            '仙狐彩袂' : [210144,210145,210206,210207],
            '玄素天成' : [21121,21122,21123,21124,21326,21327,88326,88327],
            '岸芷汀兰' : [21335,21336,121529,121530],
            '蝶恋清梦' : [121759,121760],
            '剑气箫心' : [121813,121814],
            '化蝶成双' : [121933,121934,121935,121936,121937],
            '岁月静好' : [121989,121990,121991,121992,121993,121994,121995,121996],
            '露萤清夜' : [122011,122012],
            '游园惊梦' : [122137,122138],   #从此处开始为新增永久，官网没有统计
            '绝代风华' : [122260,122261],
            '幽都月明' : [200001]    #id杜撰的
            }
riders = {
#            '凯枫儿' : [21968],
#            '金乌展翼' : [21818],
#            '地载万物' : [21610,21682],
#            '新燕双飞' : [21648],
#            '大无尾熊' : [21884],
#            '一苇渡江' : [21687],
            '御风儿' : [21969],
#            '雪羽惊鸿' : [21638],
            '一叶扁舟' : [21665,21755,21858],
#            '冰吼' : [21605,21607,21612],
#            '池中方圆' : [215110],
#            '狰' : [21880],
            '玉鸡子' : [21934,215186],
#            '东皇太鸡' : [21935],
            '黄泉不系' : [21577,21767],
#            '玄龙狂鲨' : [21627],
#            '鹿鸣梅语' : [215151],
#            '戾天山尊' : [21611,21836,215166,215167,215168,215169,215170],
#            '幽狼' : [21982,21994,21995,21996,21997,215179,215180,215181,215182,215183,215184],
#            '飞天貔貅' : [21613,21899],
            '月华浮光' : [21688],
#            '玄海虎鲨' : [21628],   
            '海棠儿' : [21967],  
            '豚豚' : [21655,21737],
            '鲤跃龙腾' : [215404],   #俗称跑车
            '战火燎原' : [215305],   #俗称自行车
            '升龙变' : [21999],
            '御龙腾' : [215211],
            '萌眸善睐' : [215124],
            '策马扬鞭' : [21883],
            '长河落日' : [215324],
            '少年飞驰' : [215187],
            '雷之梦境守护' : [100001],
            '游龙变' : [100002],
            '梦境之主' : [100003],
            '星辰变' : [100004],
            '以梦为马' : [100005]
        }
mengPai = {
        30 : '荒火',
        31 : '天机',
        32 : '翎羽',
        33 : '魍魉',
        34 : '太虚',
        35 : '云麓',
        36 : '冰心',
        37 : '弈剑',
        38 : '鬼墨',
        39 : '龙巫',
        41 : '幽篁'             
        }

##获取特殊时装
def GetSpecialClothes(list):
    special = []    
    for x in clothes:
        if (set(clothes[x]) & set(list)):
            special.append(x)
    return special

##获取特殊珍兽
def GetSpecialRider(list):
    special = []
    for x in riders:
        if (set(riders[x]) & set(list)):
            special.append(x)
    return special
    
##获取门派
def GetMengPai(id):
    if id in mengPai:
        return mengPai[id]
    else:
        return '未知'

##获取山河画卷属性
def GetShanhe(soup):
    shanheHuajuan = []
    for i in range(0,len(soup.select('.detail_wrap_block'))):
        if '山河画卷' in soup.select('.detail_wrap_block')[i].text: #山河图与装备的关键字不同，单独分析
            shanheHuajuan.append(soup.select('.detail_wrap_block')[i].select('.tx3TextBlock')[0]['tx3text'].split('#')[0].split(':')[1])
            shanheHuajuan.append(soup.select('.detail_wrap_block')[i].select('.tx3TextBlock')[0]['tx3text'].split('#')[1].split(':')[1])
            shanheHuajuan.append(soup.select('.detail_wrap_block')[i].select('.tx3TextBlock')[0]['tx3text'].split('#')[4].split(':')[1])
    return(shanheHuajuan)

#----------估值函数-----------#
global jiahuScore,lianhuScore,liankongList
#加护价值
jiahuScore = {
            0 : 0,
            144 : 100,
            180 : 300,
            234 : 1300,
            252 : 2000,
            270 : 5500,
            288 : 8000,
            324 : 15500,
            342 : 36000,
            360 : 60000
            }
#炼护价值
lianhuScore = {
            0	: 0,
            120 : 80,
            150 : 200,
            195 : 1000,
            210 : 1500,
            225 : 4000,
            240 : 8500,
            270 : 15000,
            285 : 32000,
            300 : 58000
            }

##钻估值
def GetJiahuValue(dic,jiahu): 
    #把key转为列表
    jiahuNum = list(dic.keys())
    for x in range(len(jiahuNum)):
        if int(jiahu) == jiahuNum[x]:
            return dic[jiahuNum[x]]
            break
        elif int(jiahu) < jiahuNum[x]:
            return int(dic[jiahuNum[x-1]]+(dic[jiahuNum[x]]-dic[jiahuNum[x-1]])*(int(jiahu)-jiahuNum[x-1])/(jiahuNum[x]-jiahuNum[x-1]))
            break
#print('人物加护价值'+str(GetJiahuValue(jiahuScore,info['加护'])))   
#print('炼护价值'+str(GetJiahuValue(lianhuScore,info['炼护'])))
#print('孩子加护价值'+str(GetJiahuValue(jiahuScore,int(info['孩子加护'])*3)/3)) 
            
#炼孔从13开始需要用天域声望开,100声望折算5元
liankongList = {
            '13' : 300,
            '14' : 300+260,
            '15' : 300+260+360,
            '16' : 300+260+360+720,
            '17' : 300+260+360+720+1080,
            '18' : 300+260+360+720+1080+1600,
            '19' : 300+260+360+720+1080+1600+2700,
            '20' : 300+260+360+720+1080+1600+2700+4050
        }
##炼护孔估值，主要是给拆钻号用的
def GetliankongValue(lianhuZuan:str,lianhuKong:str):
    if lianhuKong in liankongList:
        value1 = int(liankongList[lianhuKong]/100)*5
    else:
        value1 = 0
    if lianhuZuan in liankongList:
        value2 = int(liankongList[lianhuZuan]/100)*5
    else:
        value2 = 0
    value = value1 - value2
    if int(lianhuZuan)<=8:       
        return value
    else:
        return int((1-(int(lianhuZuan)-8)/(int(lianhuKong)-8))*value) #对于高炼护孔的装备，钻加的越多，炼护孔价值越低

            
##人物装备估值，如果价格较高，地魂套贬值越厉害，这个还没考虑进去
def GetRenwuZhuangbei(info:dict ,info2:dict):  #info是装备信息，info2是人物信息
    #xxx 每个值第一个元素表示装备等级，第二个元素表示满足条件的增值
    dengji = int(info2['等级'])
    shenqi = info2['神启境界']
    zuanGuzhi = int(info2['人物加护估值']) + int(info2['人物炼护估值'])
    if dengji <=69:
        xxx = {0:[102,100,'头盔'],1:[102,100,'上衣'],2:[102,100,'腰带'],3:[102,100,'裤子'],4:[96,200,'副手'],5:[95,100,'武器'],
               6:[91,50,'玉佩'],7:[92,60,'项链'],8:[102,100,'肩膀'],9:[102,100,'手腕'],10:[102,100,'下摆'],11:[102,100,'鞋子'],
               13:[108,100,'戒指'],14:[108,100,'戒指'],15:[91,50,'耳环'],16:[91,50,'耳环']} #17,18手镯没有金色装备不计
    elif dengji <=74:
        xxx = {0:[84,20,'头盔'],1:[84,20,'上衣'],2:[84,20,'腰带'],3:[84,20,'裤子'],4:[87,50,'副手'],5:[100,250,'武器'],
               6:[96,100,'玉佩'],7:[98,120,'项链'],8:[84,20,'肩膀'],9:[84,20,'手腕'],10:[84,20,'下摆'],11:[84,20,'鞋子'],
               13:[96,100,'戒指'],14:[96,100,'戒指'],15:[96,70,'耳环'],16:[96,70,'耳环']} #17,18手镯没有金色装备不计
    elif dengji <=79:
        xxx = {0:[88,40,'头盔'],1:[88,40,'上衣'],2:[88,40,'腰带'],3:[88,40,'裤子'],4:[96,200,'副手'],5:[108,400,'武器'],
               6:[110,200,'玉佩'],7:[110,200,'项链'],8:[88,40,'肩膀'],9:[88,40,'手腕'],10:[88,40,'下摆'],11:[88,40,'鞋子'],
               13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = {0:[92,70,'头盔'],1:[92,70,'上衣'],2:[92,70,'腰带'],3:[92,70,'裤子'],4:[96,200,'副手'],5:[108,400,'武器'],
                   6:[110,200,'玉佩'],7:[110,250,'项链'],8:[92,70,'肩膀'],9:[92,70,'手腕'],10:[92,70,'下摆'],11:[92,70,'鞋子'],
                   13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
        else:
            xxx = {0:[102,100,'头盔'],1:[102,100,'上衣'],2:[102,100,'腰带'],3:[102,100,'裤子'],4:[96,200,'副手'],5:[108,400,'武器'],
                   6:[110,200,'玉佩'],7:[110,250,'项链'],8:[102,100,'肩膀'],9:[102,100,'手腕'],10:[102,100,'下摆'],11:[102,100,'鞋子'],
                   13:[108,400,'戒指'],14:[108,400,'戒指'],15:[108,100,'耳环'],16:[108,100,'耳环']} #17,18手镯没有金色装备不计
    RenwuZhuangbei = 0
    for x in info['equ']:
        if 'equ_lv' in info['equ'][x]:
            if int(x) == 5:
                if 'break_count' in info['equ'][x]:  # 太初武器计算复杂点，因为太初贵重等级只有95
                    if info['equ'][x]['break_count'] == 3:
                        RenwuZhuangbei = RenwuZhuangbei + 200
                    elif info['equ'][x]['break_count'] == 4:
                        RenwuZhuangbei = RenwuZhuangbei + 600
                    elif info['equ'][x]['break_count'] == 5:
                        RenwuZhuangbei = RenwuZhuangbei + 6000
                elif info['equ'][x]['equ_lv'] >= xxx[int(x)][0]:
                    RenwuZhuangbei = RenwuZhuangbei + xxx[int(x)][1]  
            elif int(x) in [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16]:  
                if info['equ'][x]['equ_lv'] >= xxx[int(x)][0] and info['equ'][x]['equ_lv'] != 90:  #贪庛套贵重是90
                    RenwuZhuangbei = RenwuZhuangbei + xxx[int(x)][1]
                elif info['equ'][x]['equ_lv'] == 108 and int(x) == 7: #108级的项链也给点
                        RenwuZhuangbei = RenwuZhuangbei + 150
                elif '天魂' in shenqi:
                    if info['equ'][x]['equ_lv'] < 88: #对神启严格点，装备太差要扣
                        RenwuZhuangbei = RenwuZhuangbei - 100
                    elif info['equ'][x]['equ_lv'] >= 92 and int(x) in [0,1,2,3,8,9,10,11]: #地魂套还是适当给点,但价格贵了就要扣
                        if zuanGuzhi <= 1500:
                            RenwuZhuangbei = RenwuZhuangbei + 20
                        else:
                            RenwuZhuangbei = RenwuZhuangbei - min(200,int(80*zuanGuzhi/2300))
    return max(RenwuZhuangbei,0)

##孩子装备估值,同样的装备比人物略便宜点
def GetHaiziZhuangbei(info :dict,maxmingqi):
    HaiziZhuangbei = 0
    if maxmingqi > 0:
        for x in info['new_childs']:
            if (x['repute'] == maxmingqi):   #判断是否主娃
                if 'equs' in x:
                    for y in x['equs']:     
                        if 'equ_lv' in x['equs'][y]:
                            if int(y) == 0: #武器
                                if 'break_count' in x['equs'][y]:  
                                    if x['equs'][y]['break_count'] == 3:
                                        HaiziZhuangbei = HaiziZhuangbei + 150
                                    elif x['equs'][y]['break_count'] == 4:
                                        HaiziZhuangbei = HaiziZhuangbei + 500
                                    elif x['equs'][y]['break_count'] >= 5:
                                        HaiziZhuangbei = HaiziZhuangbei + 5000
                                elif x['equs'][y]['equ_lv'] >= 108:
                                    HaiziZhuangbei = HaiziZhuangbei + 300
                            elif int(y) in [1,2,3,4]: #铠甲
                                if x['equs'][y]['equ_lv'] >= 102:  #天魂套
                                    HaiziZhuangbei = HaiziZhuangbei + 80
                                elif x['equs'][y]['equ_lv'] >= 92: #地魂套
                                    HaiziZhuangbei = HaiziZhuangbei + 50
                            elif int(y) == 5: #项链
                                if x['equs'][y]['equ_lv'] >= 110:  #79级金色项链
                                    HaiziZhuangbei = HaiziZhuangbei + 200
                                elif x['equs'][y]['equ_lv'] == 108:  #78级金色项链
                                    HaiziZhuangbei = HaiziZhuangbei + 100
                break   
    return HaiziZhuangbei
    
##特技估值
def GetTejiValue(info:list):
    teji = info['防护特技']
    #guzhi = int(info['人物加护估值'])+int(info['人物炼护估值'])+int(info['孩子加护估值'])+int(info['人物装备估值'])+int(info['孩子装备估值'])
    value = 0
    if '护心' in teji:
        value = value + 1800
    if '完封' in teji:
        value = value + 1300
    if '火元防护' in teji:
        value = value + 150
    if '水风毒防护' in teji:
        value = value + 100
    if '钝刺防护' in teji:
        value = value + 150
    if '挥砍防护' in teji:
        value = value + 100
    if '物理防护' in teji:
        value = value + 350
    if '法术防护' in teji:
        value = value + 250
    if '伤害防护' in teji:
        value = value + 400   
    return value
#print('防护特技价值'+str(GetTejiValue(info['防护特技'])))

##时装估值,num为‘’时表示该函数用于藏宝阁，否则用于英雄榜
def GetShizhuangValue(shizhuang,num=''):
    value = 0
    if shizhuang == '' and num == '':
        return 0
    else:
        
        fenGeShizhuang = shizhuang.split('|')
        if num == '':
            value = 100*len(fenGeShizhuang)
        else:
            value = 100*int(num)
        if '黛染青花' in shizhuang:
            value = value + 500
        if '玄素天成' in shizhuang:
            value = value + 400
        if '海棠未雨' in shizhuang:
            value = value + 300
        if '绛云思暖' in shizhuang:
            value = value + 300
        if '大圣金甲' in shizhuang:
            value = value - 50
        if '幽都月明' in shizhuang:
            value = value + 300
        return value
#print('时装价值'+str(GetShizhuangValue(info['特殊时装'])))

##珍兽估值
def GetZhenshouValue(zhenshou,shuliang):
    num = int(shuliang)
    if zhenshou == '':
        value = 0
    else:
        kkk = zhenshou.split('|')
        value = 20*len(kkk)
        if '鲤跃龙腾' in zhenshou:
            value = value + 30
        if '战火燎原' in zhenshou:
            value = value + 30
        if '升龙变' in zhenshou:
            value = value + 30
        if '一叶扁舟' in zhenshou:
            value = value + 30
        if '长河落日' in zhenshou:
            value = value + 30
        if '雷之梦境守护' in zhenshou:
            value = value + 5000
    if num >= 100:
        value += 500 + 50*(int(num/10)-10)
    elif num >= 50:
        value += 100*(int(num/10)-5)
    return value    

##VIP估值,对于粉翅膀及以上，默认有VIP9，无需增值
def GetVipValue(info):
    vip = info['VIP9']
    jiahu = int(info['加护'])
    jiazhi = int(info['人物加护估值'])+int(info['人物炼护估值'])+int(info['孩子加护估值'])+int(info['人物装备估值'])+int(info['孩子装备估值'])+int(info['防护特技估值'])+int(info['特殊时装估值'])+int(info['珍兽估值'])
    if jiahu >= 288: #粉翅膀及以上默认VIP9，不增值,也不认为会降到VIP8
        return 0
    elif vip == '否':
        return min(0,int(400*max(-2,1-jiazhi/4000))) #4000以上线性递增,800封顶
    elif vip == '是':
        return max(0,int(350*(1-jiazhi/8000))) #8000以内线性递减
    else:
        return 0
#print('VIP价值'+str(GetVipValue(info['VIP9'],info['加护'])))

##元魂珠估值，暂时没有考虑融合累积
def GetZhuziValue(teshuZhu,hetiZhu):
    if teshuZhu == '':
        value1 = 0
    else:
        tempX = teshuZhu.split('|')
        value1 = 100*len(tempX)
        if '喜气洋羊' in teshuZhu:
            value1 = value1 + 500
        if '显圣真君' in teshuZhu:
            value1 = value1 + 300
    if hetiZhu == '':
        value2 = 0
    else:
        value2 = 200*len(hetiZhu.split('|'))
    return value1+value2
#print('元魂珠价值'+str(GetZhuziValue(info['特殊元魂珠'],info['天地魂合体珠'])))    

##孩子资质及武学估值，资质封顶1000,1000以上的认为是明慧点化，不计入内
def GetHaiziValue(info):
    haiziZizhi = info['孩子资质']
    haiziwuxue = int(info['孩子武学'])
    haiziJiazhi = int(info['孩子装备估值']) + int(info['孩子加护估值']) #孩子价值越高，资质的意义才越高
    if haiziwuxue == 8:
        value = 800
    elif haiziwuxue == 9:
        value = 3000
    elif haiziwuxue == 10:
        value = 10000
    else:
        value = 0
    value = value*min(1,haiziJiazhi/5000) #武学估值也得跟孩子装备挂钩
    if haiziZizhi == '没有孩子':
        return -500
    else:
        tempY = int(haiziZizhi)
        if tempY < 900:
            value = value - 50
        elif tempY < 950:
            value = value + 0
        else:
            #如果孩子装备不好，资质估值折半
            value = value + max(round(min(4*(tempY - 950),200)*min(haiziJiazhi/500,1)),round(min(4*(tempY - 950),200)/2))
        return round(value)
#print('孩子资质价值'+str(GetHaiziValue(info['孩子资质'])))

##孩子点化及天书估值
def GetDianhuaTianshu(info : dict,maxmingqi):
    dianhua = 0
    tianshu = 0
    if maxmingqi > 0:
        for x in info['new_childs']:
            if (x['repute'] == maxmingqi):   #判断是否主娃
                if 'equs' in x:
                    for y in x['equs']:     #评估点化条数
                        if 'child_inlay_props' in x['equs'][y] and 'inlay_count' in x['equs'][y]['child_inlay_props']:
                            if x['equs'][y]['child_inlay_props']['inlay_count'] == 3:
                                dianhua = dianhua + 60
                            elif x['equs'][y]['child_inlay_props']['inlay_count'] == 4:
                                dianhua = dianhua + 200 
                            elif x['equs'][y]['child_inlay_props']['inlay_count'] >= 5:
                                dianhua = dianhua + 3000
                if 'fourbooks' in x:
                    for z in x['fourbooks']: 
                        if 'th_lv' in x['fourbooks'][z]:  #评估天书级别
                            if x['fourbooks'][z]['th_lv'] >= 2:
                                tianshu = tianshu + 80*pow(2,int(x['fourbooks'][z]['th_lv'])-2)
                        if 'th_props' in x['fourbooks'][z]:  #评估天书条数
                            if len(x['fourbooks'][z]['th_props']) ==2:
                                tianshu = tianshu + 50
                            elif len(x['fourbooks'][z]['th_props']) ==3:
                                tianshu = tianshu + 120
                            elif len(x['fourbooks'][z]['th_props']) >=4:
                                tianshu = tianshu + 400
                break
    return dianhua + tianshu

##PVE等级估值
def GetPveValue(qihui,tianling,dengji):
    if qihui == '未知':
        return 0
    elif (int(qihui) < 20) and (int(dengji) >=79):
        return -100
    else:
        value1 = 0
        value2 = 0
        if int(qihui) >= 40:
            value1 = 100 + (int(qihui)-40)*20
        if int(tianling) >= 500:
            value2 = 100 + (int(tianling)-500)*2
        return int(value1/2 + value2/2)
    
##人物等级估值，对于神启角色有两套估值方案，一个是PVP一个是PVE，对于咸鱼风景副本党，等级就不是那么重要
def GetDengjiValue(info : list,flyLevel :int):  #flyLevel111-149是地魂，211-269是天魂
    dengji = int(info['等级'])
    PVPguzhi = int(info['人物加护估值'])+int(info['人物炼护估值'])+int(info['孩子加护估值'])+int(info['防护特技估值'])+int(info['元魂珠估值'])+int(info['孩子点化及天书估值'])+int(info['孩子资质及武学估值'])+int(info['人物装备估值'])+int(info['孩子装备估值'])
    #print(PVPguzhi)
    value = 0
#    if PVPjiazhi >= 1000:
#        aaa = {
#                '未神启' : -400,'地魂壹' : -200,'地魂贰' : 0,'地魂叁' : 200,'地魂肆' : 400,
#                '天魂壹' : -600,'天魂贰' : -400,'天魂叁' : -200,'天魂肆' : 0,'天魂伍' : 400,'天魂陆' : 800            
#                }
#    else:
#        aaa = {
#                '未神启' : 50,'地魂壹' : 200,'地魂贰' : 200,'地魂叁' : 250,'地魂肆' : 300,
#                '天魂壹' : 200,'天魂贰' : 350,'天魂叁' : 400,'天魂肆' : 450,'天魂伍' : 500,'天魂陆' : 600                            
#                }
    if dengji <= 59:
        value = max(0,0 - 20*(59-dengji))
    elif dengji <= 69:
        value = max(0,50 - 20*(69-dengji))
    elif dengji <=74:
        value = max(0,80 - 30*(74-dengji))
    elif dengji <=79:
        value = 120 - 40*(79-dengji)
    else:  
        if flyLevel == 0:
            PVE = 50
            PVP = -400
        elif flyLevel <= 149:
            PVE = 300+6*(flyLevel-149)   ##这里不是很严谨，因为flyLevel没有120,130,140,但误差也不大
            PVP = 400+20*(flyLevel-149)
        elif flyLevel <= 269:
            PVE = 600+10*(flyLevel-269)
            PVP = 1200 + 55*(flyLevel-269)
        else:
            PVE = 999
            PVP = 999
        if PVPguzhi < 1000:
            value = PVE
        elif PVPguzhi < 10000:  #取个中间区间，避免个别极端情况变化太陡，例如节点的边缘切换
            kkk = (PVPguzhi-1000)/9000
            value = int(PVP*(kkk) + PVE*(1-kkk))
        else:
            value = PVP
    return int(value)
#获取马丹估值
def GetMadanValue(soup):
    madan = 0
    for x in soup.select('.lingshou-box'):
        if x.select('.lingshou-desc.StarTable'):
            for i in x.select('.lingshou-desc.StarTable'):
                for j in i['tooltip_intro'].split('#'):
                    if '乾元之气等级' in j:                               
                        if int(re.sub("\D","",j)) >= 2:
                            madan = madan + 50*pow(2,int(re.sub("\D","",j))-2)  #模仿天书等级评估，打点折扣
                        mmm = i['tooltip_intro'][i['tooltip_intro'].find('乾元之气等级'):].count('#r#c')-1  #最后有个图文属性不用计算在内   
                        if mmm == 2:
                            madan = madan + 40
                        elif mmm == 3:
                            madan = madan + 100
                        elif mmm >= 4:
                            madan = madan + 300
    return madan

#灵兽七曜星盘估值，xingpan格式 ['太阳63-111','太阴69-021','晨星64-120','太白73-120','荧惑64-021','岁星69-120']
def GetQiyaoxingpanValue(xingpan:list):
    xingpanValue = 0
    for z in xingpan:
        #用幂函数0.6102*1.363**(等级-60)模拟确定底价，然后中/2，高*1.5，究*4，累计，底价+1是为了60级的底价从2开始
        xingdianLevel = int(z[2:].split('-')[0])
        if xingdianLevel >= 60:
            jiage = (round(0.6102*1.363**(xingdianLevel-60))+1)*(int(z[2:].split('-')[1][0])/2 + int(z[2:].split('-')[1][1])*1.5 + int(z[2:].split('-')[1][2])*4)
            xingpanValue = xingpanValue + jiage 
    return int(xingpanValue*0.6) #马灵化材料降价了，打个6折

##声望估值
def GetShengwangValue(junzi,wangchao):
    value = 0
    junzi = int(junzi)
    wangchao = int(wangchao)
    if junzi >= 1000:
        value = int(junzi/1000*30)+value
    if wangchao>=250:
        value = value + wangchao//250*15
    return value

##山河画卷估值,192,161,124,90按照强化百分比分4档
def GetHuajuan(huajuan:list):
    if len(huajuan) < 3:
        value = 0
    else:
        HuajuanDengji = int(huajuan[0])
        Pingfen = int(huajuan[1])
        Baifenbi = float(huajuan[2][:-1])/100
        #print(HuajuanDengji,Pingfen,Baifenbi)
        #初始评分有800，折中减去600再进行评估  (Pingfen -600 - HuajuanDengji*170)
        if Baifenbi >= 1.92:
            value = int(max(0,(Pingfen - 600 - HuajuanDengji*170))*(3+(Baifenbi-1.92)*5)/100)*100
        elif Baifenbi >= 1.61:
            value = int(max(0,(Pingfen - 600 - HuajuanDengji*170))*(1.61+(Baifenbi-1.61)*2)/100)*100
        elif Baifenbi >= 1.24:
            value = int(max(0,(Pingfen - 600 - HuajuanDengji*170))*(1.24+(Baifenbi-1.24)*1)/100)*100          
        else:
            value = int(max(0,(Pingfen - 600 - HuajuanDengji*170))*max(0,(1.24-(1.24-Baifenbi)*1.2))/100)*100
        if value <= 100 and Baifenbi >= 0.3: #靠时间刷出来的等级还是适当给点
            value += min(int(HuajuanDengji/10*100*Baifenbi),400)
    return value
#print(GetHuajuan(['46','9000','95%']),GetHuajuan(['28','9124','192%']),GetHuajuan(['19','5814','116%']),GetHuajuan(['38','15400','167%']),GetHuajuan(['22','4050','33%']),GetHuajuan(['23','7800','125%']))
#print(GetHuajuan(['35','6343','52%']))

##攻击期望,等级门派相同、估值相近的前提下,与大小攻、会心重击、诛心万钧人祸有关
def GetGongjiQiwang(info : list,u='fromCBG'):
    def Huixinlv(dengji : int,shenqi : str,huixin : int):
        if dengji <=59:
            return round(huixin/2120,3)
        elif dengji <=69:
            return round(huixin/2520,3)
        elif dengji <=74:
            return round(huixin/2800,3)
        elif dengji <=79:
            return round(huixin/3000,3)
        elif dengji == 80:
            if '地魂' in shenqi:
                return round(huixin/3830,3)
            else:
                return round(huixin/4500,3)
    #重击率可以套用会心率的函数，结果X2
    dengji = int(info['等级'])
    shenqi = info['神启境界'] 
    huixin = int(info['会心'])
    zhongji = int(info['重击'])
    if info['门派'] == '翎羽' and u == 'fromYXB':  #英雄榜上翎羽有玄修加成小攻上升20%,还原成原始攻击
        if int(info['最小物攻'])/int(info['最大物攻']) > 0.9:
            zuixiaoWugong = int(int(info['最小物攻'])/1.2)
            zuidaWugong = int(int(info['最大物攻'])/1.2)
        else:
            zuixiaoWugong = int(int(info['最小物攻'])/1.2)
            zuidaWugong = int(info['最大物攻'])
    else:
        zuixiaoWugong = int(info['最小物攻'])
        zuidaWugong = int(info['最大物攻'])
    zuixiaoFagong = int(info['最小法攻'])
    zuidaFagong = int(info['最大法攻'])
    mengpai = info['门派']
    if '性别' in info:
        xingbie = info['性别']
    elif (zuixiaoWugong+zuidaWugong)>=(zuixiaoFagong+zuidaFagong):  #英雄榜没有提供性别，但对于龙巫来说性别很重要，用攻击力来判断男女
        xingbie = '男'
    else:
        xingbie = '女'
    renhuo = float(info['人祸'])
    zhuxin = float(info['诛心'])
    wanjun = float(info['万钧'])
    fushang = float(info['附伤'])
    GongJiQiwang = 0
    if mengpai == '翎羽':     #翎羽有加20%小攻的玄修
        zuixiaoWugong = zuixiaoWugong*1.2
        zuidaWugong = max(zuixiaoWugong,zuidaWugong)
    ##计算伤害期望
    if (mengpai in ['魍魉','翎羽','荒火','天机']) or (mengpai == '龙巫' and xingbie == '男') or (mengpai == '弈剑' and zuidaWugong > zuidaFagong):
        GongJi_huixin = (zuidaWugong+fushang)*1.5*Huixinlv(dengji,shenqi,huixin)*100*(1+renhuo/100)*(1+zhuxin/18/100)  #100次攻击的会心伤害期望
        GongJi_zhongji = ((zuixiaoWugong+zuidaWugong)/2*2+fushang)*Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100)*(1+renhuo/100)*(1+wanjun/18/100)  #除去会心次数，剩余攻击中的重击伤害期望
        GongJi_putong = ((zuixiaoWugong+zuidaWugong)/2+fushang)*max(100-Huixinlv(dengji,shenqi,huixin)*100-Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100),0)*(1+renhuo/100)  #除去重击和会心次数，剩余普通攻击的伤害期望
        GongJiQiwang = (GongJi_huixin + GongJi_zhongji + GongJi_putong)/100  
    elif mengpai in ['云麓','太虚','冰心','鬼墨'] or (mengpai == '龙巫' and xingbie == '女') or (mengpai == '弈剑' and zuidaWugong < zuidaFagong):
        zuidaGongji = zuidaFagong
        zuixiaoGongji = zuixiaoFagong
        GongJi_huixin = zuidaGongji*1.5*Huixinlv(dengji,shenqi,huixin)*100*(1+renhuo/100)*(1+zhuxin/18/100)  #100次攻击的会心伤害期望
        GongJi_zhongji = (zuixiaoGongji+zuidaGongji)/2*2*Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100)*(1+renhuo/100)*(1+wanjun/18/100)  #除去会心次数，剩余攻击中的重击伤害期望
        GongJi_putong = (zuixiaoGongji+zuidaGongji)/2*max(100-Huixinlv(dengji,shenqi,huixin)*100-Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100),0)*(1+renhuo/100)  #除去重击和会心次数，剩余普通攻击的伤害期望
        GongJiQiwang = (GongJi_huixin + GongJi_zhongji + GongJi_putong)/100  
    elif mengpai == '幽篁':  #幽簧可以双修，所以附伤的权重要看是法攻幽簧还是物攻幽簧
        if zuidaFagong*1.2 < zuidaWugong:
            zuidaGongji = max(zuidaWugong,zuidaFagong)+0.2*min(zuidaWugong,zuidaFagong)+fushang   #幽篁是同时物法双系伤害
            zuixiaoGongji = max(zuixiaoWugong,zuixiaoFagong)+0.2*min(zuixiaoWugong,zuixiaoFagong)+fushang
        elif zuidaWugong*1.2 < zuidaFagong:
            zuidaGongji = max(zuidaWugong,zuidaFagong)+0.2*min(zuidaWugong,zuidaFagong)+fushang/2   #幽篁是同时物法双系伤害
            zuixiaoGongji = max(zuixiaoWugong,zuixiaoFagong)+0.2*min(zuixiaoWugong,zuixiaoFagong)+fushang/2
        else:
            zuidaGongji = max(zuidaWugong,zuidaFagong)+0.2*min(zuidaWugong,zuidaFagong)+fushang*3/4   #幽篁是同时物法双系伤害
            zuixiaoGongji = max(zuixiaoWugong,zuixiaoFagong)+0.2*min(zuixiaoWugong,zuixiaoFagong)+fushang*3/4
        GongJi_huixin = zuidaGongji*1.5*Huixinlv(dengji,shenqi,huixin)*100*(1+renhuo/100)*(1+zhuxin/18/100)  #100次攻击的会心伤害期望
        GongJi_zhongji = (zuixiaoGongji+zuidaGongji)/2*2*Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100)*(1+renhuo/100)*(1+wanjun/18/100)  #除去会心次数，剩余攻击中的重击伤害期望
        GongJi_putong = (zuixiaoGongji+zuidaGongji)/2*max(100-Huixinlv(dengji,shenqi,huixin)*100-Huixinlv(dengji,shenqi,zhongji)*2*(100-Huixinlv(dengji,shenqi,huixin)*100),0)*(1+renhuo/100)  #除去重击和会心次数，剩余普通攻击的伤害期望
        GongJiQiwang = (GongJi_huixin + GongJi_zhongji + GongJi_putong)/100    
    if mengpai == '弈剑' and zuidaWugong > zuidaFagong:  # 弈剑堆物攻比法攻难,而且有幻心加成33%,同装评攻击期望上浮20%
        GongJiQiwang = GongJiQiwang*1.2   
    return round(GongJiQiwang,1)

##金色属性综合增值
def GetJinseShuxing(info : list):
    zhuidian = round((int(info['追电'])-330)/330*100,1)  #移动提升多少百分点
    jiyu = int(info['疾语'])
    zuixiaoWugong = int(info['最小物攻'])
    zuidaWugong = int(info['最大物攻'])
    zuixiaoFagong = int(info['最小法攻'])
    zuidaFagong = int(info['最大法攻'])
    if '性别' in info:
        xingbie = info['性别']
    elif (zuixiaoWugong+zuidaWugong)>=(zuixiaoFagong+zuidaFagong):  #英雄榜没有提供性别，但对于龙巫来说性别很重要，用攻击力来判断男女
        xingbie = '男'
    else:
        xingbie = '女'
    if info['门派'] == '魍魉':
        zhouyu = round((int(info['骤雨'])-42)/42*100,1)  #攻速提升多少百分点
    elif info['门派'] == '荒火':
        zhouyu = round((int(info['骤雨'])-19)/19*100,1)
    elif info['门派'] in ['天机','翎羽']:
        zhouyu = round((int(info['骤雨'])-24)/24*100,1)
    elif info['门派'] == '龙巫' and xingbie == '男':
        zhouyu = round((int(info['骤雨'])-30)/30*100,1)
    elif info['门派'] == '弈剑':
        zhouyu = round((int(info['骤雨'])-30)/30*100,1)
    else:
        zhouyu = 0
    #根据门派不同，返回金色属性增值
    if info['门派'] in ['天机','荒火','翎羽']:
        return zhuidian + zhouyu/2
    elif info['门派'] in ['云麓','冰心','太虚','幽篁','鬼墨']:
        return zhuidian + jiyu
    elif info['门派'] == '魍魉':  #魍魉有自爆流
        if jiyu > 20:
            return jiyu
        else:
            return zhuidian + zhouyu/2
    elif info['门派'] == '龙巫':
        if xingbie == '男':
            return zhuidian + zhouyu/2
        else:
            return zhuidian + jiyu
    else:
        return zhuidian + jiyu + zhouyu/2    #弈剑三速都有用
    
##计算综合防御
def GetFangyu(info:list,u='fromCBG'):
    if info['门派'] == '天机' and u == 'fromYXB': #天机英雄榜上的法防和物防有三玄修加成，因为是与CBG数据做比较，为了公平起见取消加成
        wufang = int((100*int(info['物防'])-10*int(info['法防']))/99)
        fafang = int((100*int(info['法防'])-10*int(info['物防']))/99)
    else:
        wufang = int(info['物防'])
        fafang = int(info['法防'])
    shenming = int(info['神明'])
    huibi = int(info['回避'])
    zhibi = float(info['知彼'])/100
    yuxin = float(info['御心'])/18/100
    tiebi = float(info['铁壁'])/18/100
    xueliang = float(info['生命'])
    #return (wufang + fafang + shenming/0.7 + huibi/1.5 + xueliang/4.2)*(1 + zhibi + yuxin/2 + tiebi/2)  #一点念0.7神明，一点疾1.5回避，一点体平均4.2血-----采用换算成属性点的方式来评估防御属性
    return int((wufang + fafang + shenming/0.7 + huibi/1.5 + xueliang*(1/max(0.2,(1-zhibi - yuxin/2 - tiebi/2)))/2)*0.7)

###获取流派,金色|攻击|防御|暴击|攻受
def GetLiupai(info:list):
    liupai = []
    zhuidian = round((int(info['追电'])-330)/330*100,1)  #移动提升多少百分点
    jiyu = int(info['疾语'])
    if info['门派'] == '魍魉':
        zhouyu = round((int(info['骤雨'])-42)/42*100,1)  #攻速提升多少百分点
    elif info['门派'] == '荒火':
        zhouyu = round((int(info['骤雨'])-19)/19*100,1)
    elif info['门派'] in ['天机','翎羽']:
        zhouyu = round((int(info['骤雨'])-24)/24*100,1)
    elif info['门派'] == '龙巫':
        zhouyu = round((int(info['骤雨'])-30)/30*100,1)
    elif info['门派'] == '弈剑':
        zhouyu = round((int(info['骤雨'])-30)/30*100,1)
    else:
        zhouyu = 0
    zuidaWugong = int(info['最大物攻'])
    zuidaFagong = int(info['最大法攻'])
    zuixiaoWugong = int(info['最小物攻'])
    zuixiaoFagong = int(info['最小法攻'])
    wufang = int(info['物防'])
    fafang = int(info['法防'])
    huixin = int(info['会心'])
    zhongji = int(info['重击'])
    gongjiQiwang = int(float(info['攻击期望']))
    fangyuQiwang = int(float(info['综合防御']))
    if fangyuQiwang/gongjiQiwang >= 12:
        if zhuidian == max(zhuidian,jiyu,zhouyu) and zhuidian >= 15:
            liupai.append('追电')
        elif jiyu == max(zhuidian,jiyu,zhouyu) and jiyu >= 15:
            liupai.append('疾语')
        liupai.append('受')
    else:
        if zhuidian >= 1.2*jiyu and zhuidian >= 15:
            liupai.append('追电')
        elif jiyu >= 1.2*zhuidian and jiyu >= 15:
            liupai.append('疾语')
        elif zhuidian >= 15 and jiyu >= 15:
            liupai.append('双速')
        if huixin/2 >= 1.5*zhongji:
            liupai.append('会心')
        elif zhongji >= 1.5*huixin/2:
            liupai.append('重击')
        else:
            liupai.append('双暴')    
        if zuidaWugong >= 1.2*zuidaFagong:
            liupai.append('物理')
        elif zuidaFagong >= 1.2*zuidaWugong:
            liupai.append('法术')
        else:
            liupai.append('双修')
        if wufang >= 1.3*fafang:
            liupai.append('物防')
        elif fafang >= 1.3*wufang:
            liupai.append('法防')
        else:
            liupai.append('双防')
        if fangyuQiwang/gongjiQiwang >= 6:
            liupai.append('庸')
        elif ('物理' in liupai and zuixiaoWugong >= 0.9*zuidaWugong) or ('法术' in liupai and zuixiaoFagong >= 0.9*zuidaFagong):
            liupai.append('攻小')
        else:
            liupai.append('攻大')
    return '|'.join(liupai)
    
    
    
##人物的装备贵重等级
#def GetRenwuZhuangbei(info : dict):
#    ZhuangbeiDengji = 0
#    ##获取人物装备等级
#    for x in info['equ']:
#        if 'equ_lv' in info['equ'][x]:
#            if int(x) == 5 and 'break_count' in info['equ'][x]:  # 武器计算复杂点，因为太初贵重等级只有95
#                if info['equ'][x]['break_count'] == 1:
#                    ZhuangbeiDengji = ZhuangbeiDengji + 80
#                elif info['equ'][x]['break_count'] == 2:
#                    ZhuangbeiDengji = ZhuangbeiDengji + 95
#                elif info['equ'][x]['break_count'] == 3:
#                    ZhuangbeiDengji = ZhuangbeiDengji + 108
#                elif info['equ'][x]['break_count'] == 4:
#                    ZhuangbeiDengji = ZhuangbeiDengji + 120
#                else:
#                    ZhuangbeiDengji = ZhuangbeiDengji + 200
#            elif int(x) <= 18: 
#                ZhuangbeiDengji = ZhuangbeiDengji + info['equ'][x]['equ_lv']
#        elif 'reqlv' in info['equ'][x]:  # 部分装备JSON信息里没有贵重等级（副本装，低阶战场装），就计算必要等级
#            ZhuangbeiDengji = ZhuangbeiDengji + info['equ'][x]['reqlv']
#    return int(ZhuangbeiDengji)

    
#----------调整因子函数-----------#(其实可以融合成一个函数，多传一个参数就行)
##修为调整因子，在同等级同门派同总价位的情况下比较修为
def XiuweiTiaozheng(conn,info : list):
    dengji = int(info['等级'])
    shenqi = info['神启境界']
    xiuwei = int(info['修为'])
    ZongGuzhi = int(info['硬件估值总和'])+int(info['软件估值总和']) 
    mengPai = info['门派']
    Cursor = conn.cursor()
    if int(dengji) <=59:
        xxx = '等级<=59'
    elif int(dengji) <=69:
        xxx = '等级>59 and 等级<=69'
    elif int(dengji) <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif int(dengji) <=79:
        xxx = '等级>74 and 等级<=79'
    elif int(dengji) == 80:
        if '天魂' in shenqi:
            xxx = '神启境界 LIKE "%%天魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%地魂%%"'
    ZongGuzhi = int(ZongGuzhi)
    if ZongGuzhi < 5000:
        para_1 = (ZongGuzhi*0.9,ZongGuzhi*1.2)      #和稍高的号比较，要加分不要这么容易
    else:
        para_1 = (int(ZongGuzhi)*0.95,int(ZongGuzhi)*1.15)
    #sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和>=%s and 硬件估值总和<=%s and 门派='"%para_1 + mengPai + "' and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 价格>=%s and 价格<=%s AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5 and 门派='"%para_1 + mengPai + "'"
    qqq = Cursor.execute('SELECT 修为 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值和部分低值，取中间区域的平均值
        sql_2 = 'SELECT (SUM(修为)-(SELECT SUM(low.修为) FROM (SELECT 修为 '+sql_tiaojian+' ORDER BY 修为 ASC LIMIT '+str(int(qqq/2)-Number)+')low)-(SELECT SUM(high.修为) FROM (SELECT 修为 '+sql_tiaojian+' ORDER BY 修为 DESC LIMIT '+str(Number)+')high))/(COUNT(修为)-'+str(int(qqq/2))+') as 均价 '+sql_tiaojian
        Cursor.execute(sql_2)
        Pingjun = int(Cursor.fetchall()[0][0])  
        Cursor.close()
        if xiuwei >= Pingjun:
            return min(round(int(xiuwei)/Pingjun,3),1.12) #向上封顶1.2
        else:
            return max(round(int(xiuwei)/Pingjun,3),0.88) #向下封顶0.8
    else:
        return 0
   
##装评调整因子，在同等级同门派同总价位的情况下比较装评
def ZhuangpingTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    shenqi = info['神启境界']
    zhuangping = int(info['装评'])
    ZongGuzhi = int(info['硬件估值总和'])+int(info['软件估值总和']) 
    mengPai = info['门派']
    Cursor = conn.cursor()
    if int(dengji) <=59:
        xxx = '等级<=59'
    elif int(dengji) <=69:
        xxx = '等级>59 and 等级<=69'
    elif int(dengji) <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif int(dengji) <=79:
        xxx = '等级>74 and 等级<=79'
    elif int(dengji) == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
    if ZongGuzhi <= 5000:
        para_1 = (ZongGuzhi*0.9,ZongGuzhi*1.2)  #和稍高的号比较，要加分不要这么容易
    else:
        para_1 = (ZongGuzhi*0.95,ZongGuzhi*1.15) 
    #sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和>=%s and 硬件估值总和<=%s and 门派='"%para_1 + mengPai + "' and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 价格>=%s and 价格<=%s AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5 and 门派='"%para_1 + mengPai + "'"
    qqq = Cursor.execute('SELECT 装评 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值和部分低值，取中间区域的平均值
        sql_2 = 'SELECT (SUM(装评)-(SELECT SUM(low.装评) FROM (SELECT 装评 '+sql_tiaojian+' ORDER BY 装评 ASC LIMIT '+str(int(qqq/2)-Number)+')low)-(SELECT SUM(high.装评) FROM (SELECT 装评 '+sql_tiaojian+' ORDER BY 装评 DESC LIMIT '+str(Number)+')high))/(COUNT(装评)-'+str(int(qqq/2))+') as 均价 '+sql_tiaojian
        Cursor.execute(sql_2)
        Pingjun = int(Cursor.fetchall()[0][0]) 
        Cursor.close()
        if zhuangping >= Pingjun:
            return min(round(int(zhuangping)/Pingjun,3),1.1) #向上封顶1.2
        else:
            return max(round(int(zhuangping)/Pingjun,3),0.9) #向下封顶0.8
    else:
        return 0

##门派调整因子，在相近总修为的前提下，与角色等级、门派有关
def MengpaiTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    zongXiuwei = int(info['修为']) + int(info['装评'])
    mengPai = info['门派']
    shenqi = info['神启境界']
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
    sql_1 = 'FROM tx3 WHERE ' + xxx + ' and (装评+修为)>=%s and (装评+修为)<=%s and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)'
    sql_3 = 'FROM tx3 WHERE ' + xxx + ' and (装评+修为)>=%s and (装评+修为)<=%s and 门派=%s and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)'
    para_1 = (zongXiuwei*0.9,zongXiuwei*1.1)
    para_3 = (zongXiuwei*0.9,zongXiuwei*1.1,mengPai)
    if Cursor.execute('SELECT 藏宝阁编号 '+sql_3,para_3) > 10:  #满足条件的账号达到10个才有统计意义,且去掉最高修为和最低修为取平均值
        sql_3 = 'SELECT (SUM(价格)-MAX(价格)-MIN(价格))/(COUNT(价格)-2) as JunJia '+sql_3
        Cursor.execute(sql_3,para_3)
        yyy = Cursor.fetchall()
        MengpaiJunJia = int(yyy[0][0])
        #print(PingjunXiuwei)
        sql_1 = 'SELECT (SUM(价格)-MAX(价格)-MIN(价格))/(COUNT(价格)-2) as JunJia '+sql_1
        Cursor.execute(sql_1,para_1)
        xxx = Cursor.fetchall()
        SuoyouJunjia = int(xxx[0][0])    #所有角色均价的80%作为比较依据,更合理的方式应该是11个门派的均价做比较,以其中一个门派为基准      
        Cursor.close()
        return round((int(MengpaiJunJia)-SuoyouJunjia)/SuoyouJunjia,3)+1
    else:
        return 0        
        
##攻击属性调整函数, 同等级同门派同硬件估值同攻受下，与攻击期望有关
def GongjiTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    mengPai = info['门派']
    shenqi = info['神启境界']
    guzhi = int(info['硬件估值总和'])+int(info['软件估值总和']) 
    gongji = float(info['攻击期望'])
    GongShouBili = round(float(info['综合防御'])/float(info['攻击期望']),0)
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
        yyy = 3000
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
        yyy = 3600
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
        yyy = 4000
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
        yyy = 4200 
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
            yyy = 4500
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
            yyy = 5000
    sql_1 = ' and 综合防御/攻击期望>=%s and 综合防御/攻击期望<=%s'%(GongShouBili-4,GongShouBili+4)
    if guzhi < 3000:
        para_1 = (guzhi*0.85,guzhi*1.15)
    elif guzhi < 20000:
        para_1 = (guzhi*0.9,guzhi*1.1)  
    else:
        para_1 = (guzhi*0.94,guzhi*1.06) 
    #sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和>=%s and 硬件估值总和<=%s and 门派='"%para_1 + mengPai + "' and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"+sql_1
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 价格>=%s and 价格<=%s AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5 and 门派='"%para_1 + mengPai + "'"+sql_1
    qqq = Cursor.execute('SELECT 攻击期望 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值(1份)和部分低值(3份)，取剩下区域的平均值
        sql_2 = 'SELECT (SUM(攻击期望)-(SELECT SUM(low.攻击期望) FROM (SELECT 攻击期望 '+sql_tiaojian+' ORDER BY 攻击期望 ASC LIMIT '+str(int(qqq/3)-Number)+')low)-(SELECT SUM(high.攻击期望) FROM (SELECT 攻击期望 '+sql_tiaojian+' ORDER BY 攻击期望 DESC LIMIT '+str(Number)+')high))/(COUNT(攻击期望)-'+str(int(qqq/3))+') as 均价 '+sql_tiaojian
        #print(sql_2)
        Cursor.execute(sql_2)
        PingjunGongji = int(Cursor.fetchall()[0][0])
        Cursor.close()
        #低端号攻击和防御调整因子缩小，中端号维持，高端号放大，因为越便宜属性增长越容易，越高端属性增长越难
        print('平均攻击%s,角色攻击%s'%(PingjunGongji,gongji))
        if gongji >= PingjunGongji:
            return min(round((gongji-PingjunGongji)/yyy +1,3),1.5) #向上封顶1.6
        else:
            return max(round((gongji-PingjunGongji)/yyy+1,3),0.7) #向下封顶0.7
    else:
        return 0        

##防御属性调整函数,同等级同门派同硬件估值同攻受下，与综合防御有关
def FangyuTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    mengPai = info['门派']
    shenqi = info['神启境界']
    guzhi = int(info['硬件估值总和'])+int(info['软件估值总和']) 
    fangyu = float(info['综合防御'])
    GongShouBili = min(round(float(info['综合防御'])/float(info['攻击期望']),0),30)  #封顶30，有个别拆钻的极端号会远大于30
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
        yyy = 7000
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
        yyy = 7200
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
        yyy = 7600
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
        yyy = 8000
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
            yyy = 8800
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
            yyy = 9600
    sql_1 = ' and 综合防御/攻击期望>=%s and 综合防御/攻击期望<=%s'%(GongShouBili-4,GongShouBili+4)
    if guzhi < 3000:
        para_1 = (guzhi*0.85,guzhi*1.15)
    elif guzhi < 20000:
        para_1 = (guzhi*0.9,guzhi*1.1)  
    else:
        para_1 = (guzhi*0.94,guzhi*1.06)   
    #sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和>=%s and 硬件估值总和<=%s and 门派='"%para_1 + mengPai + "' and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"+sql_1
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 价格>=%s and 价格<=%s AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5 and 门派='"%para_1 + mengPai + "'"+sql_1
    qqq = Cursor.execute('SELECT 综合防御 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))  #这个数不能=0
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值(1份)和部分低值(3份)，取剩下区域的平均值
        sql_2 = 'SELECT (SUM(综合防御)-(SELECT SUM(low.综合防御) FROM (SELECT 综合防御 '+sql_tiaojian+' ORDER BY 综合防御 ASC LIMIT '+str(int(qqq/3)-Number)+')low)-(SELECT SUM(high.综合防御) FROM (SELECT 综合防御 '+sql_tiaojian+' ORDER BY 综合防御 DESC LIMIT '+str(Number)+')high))/(COUNT(综合防御)-'+str(int(qqq/3))+') as 均价 '+sql_tiaojian
        #print(sql_2)       
        Cursor.execute(sql_2)
        Pingjun = int(Cursor.fetchall()[0][0])  #以平均属性上浮2%为基准
        Cursor.close()
        #低端号攻击和防御调整因子缩小，中端号维持，高端号放大，因为越便宜属性增长越容易，越高端属性增长越难
        print('平均防御%s,角色防御%s'%(Pingjun,fangyu))
        if fangyu >= Pingjun:            
            return min(round((fangyu-Pingjun)/yyy+1,3),1.5) #向上封顶1.5           
        else:
            return max(round((fangyu-Pingjun)/yyy+1,3),0.7) #向下封顶0.7   
    else:
        return 0  
    
##金色属性调整函数,等级门派相同、硬件估值相近的前提下,与追电疾语骤雨有关
def JinseTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    mengPai = info['门派']
    shenqi = info['神启境界']
    guzhi = int(info['硬件估值总和'])+int(info['软件估值总和']) 
    jinse = float(info['金色属性'])    
    #liupai = info['流派']
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
    if guzhi < 3000:
        para_1 = (guzhi*0.85,guzhi*1.15)
    elif guzhi < 20000:
        para_1 = (guzhi*0.9,guzhi*1.1)  
    else:
        para_1 = (guzhi*0.94,guzhi*1.06) 
    #sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 最终估值>=%s and 最终估值<=%s and 门派='"%para_1 + mengPai + "' and 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 价格>=%s and 价格<=%s AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5 and 门派='"%para_1 + mengPai + "' AND 价格<=最终估值*1.5"   
    qqq = Cursor.execute('SELECT 金色属性 '+sql_tiaojian)
    if  qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))+1
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值(1份)和部分低值(7份)，取剩下区域的平均值
        sql_2 = 'SELECT (SUM(金色属性)-(SELECT SUM(low.金色属性) FROM (SELECT 金色属性 '+sql_tiaojian+' ORDER BY 金色属性 ASC LIMIT '+str(int(qqq/2)-Number)+')low)-(SELECT SUM(high.金色属性) FROM (SELECT 金色属性 '+sql_tiaojian+' ORDER BY 金色属性 DESC LIMIT '+str(Number)+')high))/(COUNT(金色属性)-'+str(int(qqq/2))+') as 均价 '+sql_tiaojian
        #print(sql_2)        
        Cursor.execute(sql_2)
        Pingjun = int(Cursor.fetchall()[0][0])  #以平均属性为基准
        Cursor.close()
        print('平均金色%s,角色金色%s'%(Pingjun,jinse))
        if jinse >= Pingjun:
            return min(round((jinse - Pingjun)*0.015+1,3),1.3) #向上封顶1.3
        else:
            return max(round((jinse - Pingjun)*0.015+1,3),0.8) #向下封顶0.8
    else:
        return 0                  

##流派调整
def LiupaiTiaozheng(conn,info :list):
    dengji = int(info['等级'])
    mengPai = info['门派']
    shenqi = info['神启境界']  
    liupai = info['流派']    
    guzhi = int(info['硬件估值总和'])+int(info['软件估值总和'])   
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
    if guzhi < 3000:
        para_1 = (guzhi*0.85,guzhi*1.15)
    elif guzhi < 20000:
        para_1 = (guzhi*0.9,guzhi*1.1)  
    else:
        para_1 = (guzhi*0.94,guzhi*1.06) 
    #加入价格<1.5*最终估值的条件，一定程度甄别成交价,但对于自爆WL就没法
    if mengPai == '魍魉' and '疾语' in liupai:
        sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和+软件估值总和>=%s and 硬件估值总和+软件估值总和<=%s "%para_1+ "and 门派='"+mengPai+"' and 流派='"+ liupai+"' AND 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"
    else:
        sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 硬件估值总和+软件估值总和>=%s and 硬件估值总和+软件估值总和<=%s "%para_1+ "and 门派='"+mengPai+"' and 流派='"+ liupai+"' and 价格<1.5*最终估值 AND 更新时间>=DATE_SUB(CURDATE(),INTERVAL 90 DAY)"
    qqq = Cursor.execute('SELECT 价格 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))+1
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值和部分低值，取中间区域的平均值
        sql_2 = 'SELECT (SUM(价格)-(SELECT SUM(low.价格) FROM (SELECT 价格 '+sql_tiaojian+' ORDER BY 价格 ASC LIMIT '+str(Number)+')low)-(SELECT SUM(high.价格) FROM (SELECT 价格 '+sql_tiaojian+' ORDER BY 价格 DESC LIMIT '+str(Number)+')high))/(COUNT(价格)-'+str(Number)+'*2) as 均价 '+sql_tiaojian
        #sql_2 = 'SELECT (SUM(价格)-(SELECT SUM(high.价格) FROM (SELECT 价格 '+sql_tiaojian+' ORDER BY 价格 DESC LIMIT '+str(Number*2)+')high))/(COUNT(价格)-'+str(Number)+'*2) as 均价 '+sql_tiaojian
        #print(sql_2)       
        Cursor.execute(sql_2)
        LiupaiPingjun = int(Cursor.fetchall()[0][0])  #以平均属性为基准
        #求同等级同价位全门派的均值,还是要排除最高的价格和最低的价格，防止有人乱挂影响计算结果
        ttt = Cursor.execute("SELECT 价格 FROM tx3 WHERE "+xxx+" and 硬件估值总和+软件估值总和>=%s AND 硬件估值总和+软件估值总和<=%s AND 价格<1.5*最终估值"%para_1)
        #Cursor.execute("SELECT AVG(KKK.价格) as 均价 FROM (SELECT AVG(JJJ.价格) AS 价格 FROM (SELECT * FROM tx3 WHERE "+xxx+" and 硬件估值总和+软件估值总和>=%s AND 硬件估值总和+软件估值总和<=%s"%para_1 + " ORDER BY 价格 LIMIT %s,%s)JJJ WHERE "%(int(round(ttt/16,0)),ttt-int(round(ttt/16,0))*2)+xxx+" and 硬件估值总和+软件估值总和>=%s AND 硬件估值总和+软件估值总和<=%s GROUP BY 门派)KKK"%para_1)
        Cursor.execute("SELECT AVG(JJJ.价格) FROM (SELECT * FROM tx3 WHERE "+xxx+" and 硬件估值总和+软件估值总和>=%s AND 硬件估值总和+软件估值总和<=%s AND 价格<1.5*最终估值"%para_1 + " ORDER BY 价格 LIMIT %s,%s)JJJ"%(int(round(ttt/16,0)),ttt-int(round(ttt/16,0))*2))
        #print("SELECT AVG(JJJ.价格) FROM (SELECT * FROM tx3 WHERE "+xxx+" and 硬件估值总和+软件估值总和>=%s AND 硬件估值总和+软件估值总和<=%s AND 价格<1.5*最终估值"%para_1 + " ORDER BY 价格 LIMIT %s,%s)JJJ"%(int(round(ttt/16,0)),ttt-int(round(ttt/16,0))*2))
        sss = Cursor.fetchall()[0][0]
        if sss:     
            QuanmengpaiPingjun = int(sss) * 1.01  #稍微把平均数提高点，即平均数上浮一点的水平才增值
            Cursor.close()
            #print(qqq,guzhi,LiupaiPingjun,QuanmengpaiPingjun)
            if LiupaiPingjun >= QuanmengpaiPingjun:
                if mengPai == '冰心' and liupai == '疾语|受': #这是数量最多的类别，流派调整不建议超过1.08
                    return min(1.08,min(round(LiupaiPingjun/QuanmengpaiPingjun,3),1.3))
                else:
                    return min(round(LiupaiPingjun/QuanmengpaiPingjun,3),1.3) #向上封顶1.3
            else:
                return max(round(LiupaiPingjun/QuanmengpaiPingjun,3),0.7) #向下封顶0.7  
        else:
            Cursor.close()
            return 0
    else:
        return 0 
    
##市场调整金额
def ShichangTiaozheng(conn,info:list):
    dengji = int(info['等级'])
    mengPai = info['门派']
    shenqi = info['神启境界'] 
    liupai = info['流派']
    #zongxiuwei = int(info['修为'])/2+int(info['装评'])
    guzhi = int(float(info['最终估值']))
    Cursor = conn.cursor()
    if dengji <=59:
        xxx = '等级<=59'
    elif dengji <=69:
        xxx = '等级>59 and 等级<=69'
    elif dengji <=74:
        xxx = '等级>"69" and 等级<="74"'
    elif dengji <=79:
        xxx = '等级>74 and 等级<=79'
    elif dengji == 80:
        if '地魂' in shenqi:
            xxx = '神启境界 LIKE "%%地魂%%"'  #单%在PYTHON里为格式化字符，如果要输出%需要两个%
        else:
            xxx = '神启境界 LIKE "%%天魂%%"'
    if guzhi < 5000:
        para_1 = (guzhi*0.9,guzhi*1.1)
    else:
        para_1 = (guzhi*0.92,guzhi*1.08) 
    # 更新时间<=DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND 价格<=最终估值*1.5 AND 价格>=最终估值*0.5  可以认为是成交价
    sql_tiaojian = "FROM tx3 WHERE " + xxx + " and 最终估值>=%s and 最终估值<=%s "%para_1+ "and 门派='"+mengPai+"' and 流派='"+ liupai+"' and 更新时间<=DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND 价格<=最终估值*1.4 AND 价格>=最终估值*0.5"
    qqq = Cursor.execute('SELECT 价格 '+sql_tiaojian)
    if qqq > 8:  #满足条件的账号达到8个以上才有统计意义,且去掉部分最高和部分最低再取平均值
        Number = int(round(qqq/16,0))
        #sql_2是一句长MYSQL语句，实现的是去掉部分高值和部分低值，取中间区域的平均值
        sql_2 = 'SELECT (SUM(价格)-(SELECT SUM(low.价格) FROM (SELECT 价格 '+sql_tiaojian+' ORDER BY 价格 ASC LIMIT '+str(int(qqq/2)-Number)+')low)-(SELECT SUM(high.价格) FROM (SELECT 价格 '+sql_tiaojian+' ORDER BY 价格 DESC LIMIT '+str(Number)+')high))/(COUNT(价格)-'+str(int(qqq/2))+') as 均价 '+sql_tiaojian
        #print(sql_2)       
        Cursor.execute(sql_2)
        Pingjun = int(Cursor.fetchall()[0][0])  #以CBG均价为基准
        #返回同等级同流派同门派同价位的CBG均值和自身估值之差，与市场挂钩
        return int((Pingjun - guzhi)/2) 
    else:
        return 0 
    
    
info = {
       '门派' : '弈剑',
       '等级' : '80',
       '性别' : '男',
       '神启境界' : '天魂贰',
       '修为' : '71000',
       '加护' : '234',
       '炼护' : '195',
       '孩子加护' : '78',
       '防护特技' : '护心|完封',
       '特殊时装' : '玄素天成',
       '特殊元魂珠' : '显圣真君|业火',
       '天地魂合体珠' : '虎将军|杀手|水怪',
       '孩子资质' : '1050',
       '启慧等级' : '15',
       '天灵点数' : '560',
       'VIP9' : '是',
       '最大物攻' : '3800',
       '最大法攻' : '800',
       '最小物攻' : '500',
       '最小法攻' : '500',
       '会心' : '3000',
       '重击' : '0',
       '人祸' : '10',
       '诛心' : '300',
       '万钧' : '0',
       '附伤' : '00'
       }

#import pymysql    
#conn = pymysql.connect(host='localhost',port=3306,user='root',password='yhwj1234',db='zhilianzhaopin',charset='utf8')
#GongjiQiwangTiaozheng(conn,info)


###查找字典含义（为了效率，放弃去数据库检索，直接用字典函数）
#def LookForDict(key,value):
#    effectRow = cursor.execute("SELECT * FROM dict WHERE keyName=%s AND keyValue=%s",(key,value))
#    if effectRow == 1:
#        row1 = cursor.fetchone()
#        return row1[3]
#    else:
#        return None 

##输出日志
import logging
from logging import handlers
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(levelname)s: %(message)s'): #%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        #sh = logging.StreamHandler()#往屏幕上输出
        #sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        if not self.logger.handlers:    #如果handler为空则添加，否则直接输出日志。不加这句判断，会重复添加handler，也就是重复输出日志
            #self.logger.addHandler(sh) #把对象加到logger里
            self.logger.addHandler(th)