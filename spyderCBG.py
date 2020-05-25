# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 16:16:11 2018
爬天下3藏宝阁角色信息并存入数据库
20190225 ⑴最终估值钻钱保底 ⑵增加七曜星盘估值
20190313 ⑴炼护估值里增加炼护孔评估
@author: Administrator
"""
import requests,json,pymysql,time,datetime,random,logging
from bs4 import BeautifulSoup
import function as fun

###主要函数：捕获第几页-第几页的角色信息
def catchRole(pageList):
    ###链接数据库
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='yhwj1234',db='zhilianzhaopin',charset='utf8')
    cursor = conn.cursor()
    for page in pageList:
        startTime = time.time()
        try:
            wbdata = requests.get(url+'&page='+str(page),headers = header,timeout = (10,30))
        except requests.exceptions.RequestException:
            print('第'+str(page)+'页连接超时,跳过执行下一页')            
        if wbdata.status_code == 200:  #超时也会返回200？
            wbdata.encoding = 'gb2312'
            JsonData = json.loads(wbdata.text)
            Result = JsonData.get('msg')
            print('第'+str(page)+'页加载耗时：'+str(time.time()-startTime))
            for role in Result:
                MoreInfo = json.loads(role['large_equip_desc'])   #large_equip_desc键值是字符串，重新加载为JSON格式
                ###获取启慧等级
                if 'pve' in MoreInfo:
                    pve_lv = MoreInfo['pve']['pve_lv']
                    pve_talent_point = MoreInfo['pve']['pve_talent_point']            
                else:
                    pve_lv = "未知"
                    pve_talent_point = "未知"
                ###获取神启阶段
                if role['fly_level'] >= 200:
                    ShenQi = '天魂'
                elif role['fly_level'] >= 1:
                    ShenQi = '地魂'
                elif role['fly_level'] == 0:
                    ShenQi = '未神启'
                ###获取性别
                if str(role['sex']) == '1':
                    sex = '男'
                else:
                    sex = '女'
                ###获取人物和孩子装备贵重等级之和
                ZhuangbeiDengji = 0
                for x in MoreInfo['equ']:
                    if 'equ_lv' in MoreInfo['equ'][x]:
                        if int(x) == 5 and 'star' in MoreInfo['equ'][x]:  # 武器计算复杂点，因为太初贵重等级不如天域4代
                            if MoreInfo['equ'][x]['star'] == 1:
                                ZhuangbeiDengji = ZhuangbeiDengji + 80
                            elif MoreInfo['equ'][x]['star'] == 2:
                                ZhuangbeiDengji = ZhuangbeiDengji + 98
                            elif MoreInfo['equ'][x]['star'] == 3:
                                ZhuangbeiDengji = ZhuangbeiDengji + 108
                            elif MoreInfo['equ'][x]['star'] == 4:
                                ZhuangbeiDengji = ZhuangbeiDengji + 120
                            else:
                                ZhuangbeiDengji = ZhuangbeiDengji + 200
                        elif int(x) <= 18:
                            ZhuangbeiDengji = ZhuangbeiDengji + MoreInfo['equ'][x]['equ_lv']
                ###获取天地魂合体珠子
                hetiZhuzi = []
                for zhu in MoreInfo['monster_souls']:
                    treeNum = str(MoreInfo['monster_souls'][zhu]['new_tree_num'][0])
                    #9是天魂节点起点，12是地魂节点起点
                    if (treeNum != '0') and (treeNum in MoreInfo['monster_souls'][zhu]['new_tree']) :
                        if ('9' in MoreInfo['monster_souls'][zhu]['new_tree'][treeNum]) and ('12' in MoreInfo['monster_souls'][zhu]['new_tree'][treeNum]):
                            hetiZhuzi.append(MoreInfo['monster_souls'][zhu]['real_name'])
                ###获取孩子资质和加护
                childZizhi = '未知'
                childWuxue = '0'
                if 'mingqi' in role['child1']:
                    mingqi1= role['child1']['mingqi']
                else: 
                    mingqi1= 0
                if 'mingqi' in role['child2']:
                    mingqi2= role['child2']['mingqi']
                else: 
                    mingqi2= 0
                if 'mingqi' in role['child3']:
                    mingqi3= role['child3']['mingqi']
                else: 
                    mingqi3= 0
                if 'mingqi' in role['child4']:
                    mingqi4= role['child4']['mingqi']
                else:
                    mingqi4= 0
                maxMingqi = max(mingqi1,mingqi2,mingqi3,mingqi4)
                if maxMingqi == 0:
                    childZizhi = '没有孩子'
                    childJiahu = '0'
                    childWuxue = '0'
                elif maxMingqi == mingqi1:
                    childZizhi = role['child1']['zizhi']
                    childJiahu = role['child1']['jiahu']
                    childWuxue = role['child1']['wuxue']
                elif maxMingqi == mingqi2:
                    childZizhi = role['child2']['zizhi']
                    childJiahu = role['child2']['jiahu']
                    childWuxue = role['child2']['wuxue']
                elif maxMingqi == mingqi3:
                    childZizhi = role['child3']['zizhi']
                    childJiahu = role['child3']['jiahu']
                    childWuxue = role['child3']['wuxue']
                elif maxMingqi == mingqi4:
                    childZizhi = role['child4']['zizhi']
                    childJiahu = role['child4']['jiahu']
                    childWuxue = role['child4']['wuxue']
                
                ###获取VIP9，如果加护不低于288默认为VIP9
                packet = MoreInfo['inv']
                VIP9 = '否'
                if int(role['equip_jia_hu']) >= 288:
                    VIP9 = '是'
                else:
                    for key in packet:
                        if str(packet[key]['id']) == '63669':
                            VIP9 = '是'
                            break
                ###获取觉醒完封
                if 'final_skill' in MoreInfo:
                    jueXing = MoreInfo['final_skill']['subSkills']
                    #print(jueXing[6])
                    #完封ID每个门派都不同，也是醉了
                    if len(jueXing) >= 7 and (jueXing[6]['libId'] in [280,296,312,328,344,360,376,392,457,508,679]): 
                        #if jueXing[6]['valid'] == True:
                        wanFeng = int(jueXing[6]['lv'])
                    else:
                        wanFeng = 0
                    if ('6' in MoreInfo['equ']) and ('ws138' in MoreInfo['equ']['6']):   # 获取玉佩上的完封值
                        wanFeng = wanFeng + MoreInfo['equ']['6']['ws138']
                else:
                    wanFeng = 0
                ###获取特技
                equipSkill = []
                equip = MoreInfo['equ']
                huXin,huoyuanFanghu,dunciFanghu,huikanFanghu,fengshuiduFanghu,quxiSanhui = 0,0,0,0,0,0
                ##大翅膀通溟上也有可能存在防护特技
                if '护心' in MoreInfo['wing_inlay_prop']:
                    huXin = 3
                elif '钝刺防护' in MoreInfo['wing_inlay_prop']:
                    dunciFanghu = 3
                elif '挥砍防护' in MoreInfo['wing_inlay_prop']:
                    huikanFanghu = 3
                elif '火元防护' in MoreInfo['wing_inlay_prop']:
                    huoyuanFanghu = 3
                elif '水风毒防护' in MoreInfo['wing_inlay_prop']:
                    fengshuiduFanghu = 3
                elif '驱邪散秽' in MoreInfo['wing_inlay_prop']:
                    quxiSanhui = 10
                    
                for k in equip:
                    if 'ws38' in equip[k]:
                        huXin = huXin + equip[k]['ws38']
                    if 'ws50' in equip[k]:
                        huoyuanFanghu = huoyuanFanghu + equip[k]['ws50']
                    if 'ws48' in equip[k]:
                        dunciFanghu = dunciFanghu + equip[k]['ws48']
                    if 'ws47' in equip[k]:
                        huikanFanghu = huikanFanghu + equip[k]['ws47']
                    if 'ws53' in equip[k]:
                        fengshuiduFanghu = fengshuiduFanghu + equip[k]['ws53']
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
                ###获取炼护孔估值
                lianhukongValue = 0
                for kk in equip:
                    if 'ep2_enh' in equip[kk] and 'ep2_slot' in equip[kk]:
                        #print(equip[kk]['ep2_enh'],equip[kk]['ep2_slot'])
                        lianhukongValue += fun.GetliankongValue(str(equip[kk]['ep2_enh']),str(equip[kk]['ep2_slot']))
                    elif 'ep2_slot' in equip[kk]:
                        #print(0,equip[kk]['ep2_slot'])
                        lianhukongValue += fun.GetliankongValue('0',str(equip[kk]['ep2_slot']))
                #print(lianhukongValue)
                ###获取永久时装列表（有部分新永久官网接口上没统计，需从时装衣橱和时装装备里去获取）
                SpecialClothes = role['special_clothes']
                if 'commode' in MoreInfo:
                    commode = MoreInfo['commode']
                    for x in commode: 
                        if commode[x]['id'] in [122137,122138,122260,122261]:
                           SpecialClothes.append(commode[x]['id'])
                if ('19' in MoreInfo['equ']) and (MoreInfo['equ']['19']['id'] in [122137,122138,122260,122261]):
                    SpecialClothes.append(MoreInfo['equ']['19']['id']) 
                if ('20' in MoreInfo['equ']) and (MoreInfo['equ']['20']['id'] in [122137,122138,122260,122261]):
                    SpecialClothes.append(MoreInfo['equ']['20']['id']) 
       
                ###获取特殊珍兽列表
                SpecialRider = role['special_rider']
                if 'saddle_tips' in MoreInfo:
                    riderNumber = len(MoreInfo['saddle_tips'])
                    #SpecialRider = list(MoreInfo['saddle_tips'].key())  #特殊珍兽列表也可以直接在MoreInfo里获取
                else:
                    riderNumber = 0
                
                ###获取七曜星盘
                qiyaoXingpanToal = []
                for x in MoreInfo['hbs']: #遍历每匹灵兽
                    Xingpan = []
                    for y in MoreInfo['hbs'][x]['hb_equ']: #遍历每个星点
                        if 'hb_equ_item_lv' in y and y['hb_equ_star'] == 3 and y['hb_equ_item_lv']>=60: #筛选出不低于60级的紫色星点
                            strZGJ = []
                            for z in y['hb_totolattr']: #获取中高究
                                strZGJ.extend(y['hb_totolattr'][z])
                            Xingpan.append(str(x)+'号'+str(y['hb_equ_item_lv'])+'-'+str(strZGJ.count(2))+str(strZGJ.count(3))+str(strZGJ.count(4)))
                    if len(Xingpan)>=5: #至少满足5个星点才算钱
                        qiyaoXingpanToal.extend(Xingpan)
                    
                    
                ###高级号从英雄榜获取山河画卷和灵兽乾元丹，低级号忽略
                shanheHuajuan = []
                madanValue = 0
                if role['price']/100 > 15000:
                    try:
                        url_yxb = 'http://bang.tx3.163.com/bang/get_role?name='+str(role['equip_name'])+'&server='+str(role['server_name'])        
                        reqHigh = requests.get(url_yxb,headers = header,timeout = (10,30))
                        if reqHigh.status_code == 200:
                            soup = BeautifulSoup(reqHigh.text,'lxml')
                            shanheHuajuan = fun.GetShanhe(soup)
                            madanValue = fun.GetMadanValue(soup)
                    except requests.exceptions.RequestException:
                        shanheHuajuan = []
                        madanValue = 0
      
                ###获取当前时间
                now = datetime.datetime.now()
                
                ###后面的join方法需要list全是字符串，所以要用str转换一下        
                info = {
                    '藏宝阁编号' : str(role['equipid']),
                    '服务器' : str(role['server_name']),
                    '角色名称' : str(role['equip_name']),
                    '门派' : fun.GetMengPai(role['kindid']),
                    '性别' : sex,
                    '等级' : str(role['equip_level']),
                    '神启境界' : ShenQi + MoreInfo['fly_soul_lv'],
                    '修为' : str(role['xiuwei']),
                    '装评' : str(role['equ_xiuwei']),
                    '加护' : str(role['equip_jia_hu']),
                    '炼护' : str(role['equip_lian_hu']),
                    '价格' : str(role['price']/100),
                    '生命' : str(role['mhp']),
                    '物防' : str(role['pdef']),
                    '法防' : str(role['mdef']),
                    '知彼' : str(role['defhuman']),
                    '回避' : str(role['avoid']),
                    '神明' : str(role['shenming']),
                    '最大物攻' : str(role['pattack_max']),
                    '最大法攻' : str(role['mattack_max']),
                    '最小物攻' : str(role['pattack_min']),
                    '最小法攻' : str(role['mattack_min']),
                    '附伤' : str(role['attadd']),
                    '命中' : str(role['hit']),
                    '会心' : str(role['critical']),
                    '重击' : str(role['modadd']),
                    '追电' : str(role['movespeed']),
                    '骤雨' : str(role['attackspeed']),
                    '疾语' : str(role['castspeed']),
                    '人祸' : str(role['attackhuman']),
                    '万钧' : str(role['wan_jun']),
                    '铁壁' : str(role['tie_bi']),
                    '诛心' : str(role['zhu_xin']),
                    '御心' : str(role['yu_xin']),
                    '山河画卷' : '|'.join(shanheHuajuan),
                    '七曜星盘' : '|'.join(qiyaoXingpanToal),
                    '王朝军资' : str(role['wang_chao_jun_zi']),
                    '天域声望' : str(role['wang_chao_tian_yu']),
                    '启慧等级' : str(pve_lv),
                    '天灵点数' : str(pve_talent_point),
                    '特殊元魂珠' : "|".join(role['pet_special_kind']),
                    '天地魂合体珠' : "|".join(hetiZhuzi),
                    '孩子资质' : str(childZizhi),
                    '孩子武学' : str(childWuxue),
                    '孩子加护' : str(childJiahu),
                    'VIP9' : VIP9,
                    '防护特技' : "|".join(equipSkill),
                    '特殊时装' : "|".join(fun.GetSpecialClothes(SpecialClothes)),
                    '特殊珍兽' : "|".join(fun.GetSpecialRider(SpecialRider)),
                    '珍兽数量' : str(riderNumber),
                    '更新时间' : datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S'),
                    'ServerId' : str(role['serverid']),
                    '藏宝阁链接' : 'https://tx3.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid={服务器ID}&equip_id={角色ID}'.format(服务器ID=role['serverid'],角色ID=role['equipid'])
                }
                #info追加估值元素
                info['人物加护估值'] = str(fun.GetJiahuValue(fun.jiahuScore,role['equip_jia_hu']))
                info['人物炼护估值'] = str(fun.GetJiahuValue(fun.lianhuScore,role['equip_lian_hu']) + lianhukongValue)
                info['孩子加护估值'] = str(int(fun.GetJiahuValue(fun.jiahuScore,int(childJiahu)*3)/3))
                info['人物装备估值'] = str(fun.GetRenwuZhuangbei(MoreInfo,info))
                info['孩子装备估值'] = str(fun.GetHaiziZhuangbei(MoreInfo,maxMingqi))
                info['防护特技估值'] = str(fun.GetTejiValue(info))
                info['特殊时装估值'] = str(fun.GetShizhuangValue(info['特殊时装']))
                info['珍兽估值'] = str(fun.GetZhenshouValue(info['特殊珍兽'],info['珍兽数量']))
                info['VIP估值'] = str(fun.GetVipValue(info))
                info['元魂珠估值'] = str(fun.GetZhuziValue(info['特殊元魂珠'],info['天地魂合体珠']))
                info['孩子资质及武学估值'] = str(fun.GetHaiziValue(info))
                info['孩子点化及天书估值'] = str(fun.GetDianhuaTianshu(MoreInfo,maxMingqi))
                info['PVE等级估值'] = str(fun.GetPveValue(pve_lv,pve_talent_point,info['等级']))
                info['人物等级估值'] = str(fun.GetDengjiValue(info,role['fly_level']))
                info['山河画卷估值'] = str(fun.GetHuajuan(shanheHuajuan))
                info['灵兽乾元丹估值'] = str(madanValue)
                info['灵兽七曜星盘估值'] = str(fun.GetQiyaoxingpanValue(qiyaoXingpanToal))
                info['声望估值'] = str(fun.GetShengwangValue(info['王朝军资'],info['天域声望']))
                if '地魂' in info['神启境界']: #地魂没开战场，除了钻钱，其余估值打个7折
                    info['硬件估值总和'] = str(int(max(0,int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])+ 0.7*(int(info['防护特技估值']) +int(info['孩子资质及武学估值']) + int(info['孩子点化及天书估值']) + int(info['人物装备估值']) + int(info['孩子装备估值'])+int(info['山河画卷估值'])+int(info['灵兽乾元丹估值'])+int(info['灵兽七曜星盘估值'])))))
                    info['软件估值总和'] = str(int(0.7*(int(info['特殊时装估值']) + int(info['珍兽估值']) + int(info['VIP估值']) + int(info['元魂珠估值']) + int(info['PVE等级估值']) +int(info['声望估值'])+int(info['人物等级估值']))))
                else:
                    info['硬件估值总和'] = str(max(0,int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])+ int(info['防护特技估值']) + int(info['孩子资质及武学估值']) + int(info['孩子点化及天书估值']) + int(info['人物装备估值']) + int(info['孩子装备估值'])+int(info['山河画卷估值'])+int(info['灵兽乾元丹估值'])+int(info['灵兽七曜星盘估值'])))
                    info['软件估值总和'] = str(int(info['特殊时装估值']) + int(info['珍兽估值']) + int(info['VIP估值']) + int(info['元魂珠估值']) + int(info['PVE等级估值']) +int(info['声望估值'])+int(info['人物等级估值']))
                info['攻击期望'] = str(fun.GetGongjiQiwang(info))
                info['综合防御'] = str(fun.GetFangyu(info))
                info['金色属性'] = str(fun.GetJinseShuxing(info))
                info['流派'] = str(fun.GetLiupai(info))
                info['修为调整因子'] = str(fun.XiuweiTiaozheng(conn,info))
                info['装评调整因子'] = str(fun.ZhuangpingTiaozheng(conn,info))
                info['门派调整因子'] = str(fun.MengpaiTiaozheng(conn,info))
                info['攻击调整因子'] = str(fun.GongjiTiaozheng(conn,info))
                info['防御调整因子'] = str(fun.FangyuTiaozheng(conn,info))
                info['金色属性调整因子'] = str(fun.JinseTiaozheng(conn,info))
                info['门派及流派调整'] = str(fun.LiupaiTiaozheng(conn,info))
#                info['装备等级调整价格'] = str(fun.ZhuangbeiDengjiTiaozheng(conn,info))
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
                #info['最终估值'] = str(max(int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值']),(int(info['硬件估值总和'])*(1+TiaozhengYinzi1)+int(info['软件估值总和']))*(1+TiaozhengYinzi2)))
                #最终估值=(钻钱+(硬件估值-钻钱)*(攻击调整+防御调整+金色调整)+软件估值)×(装评调整+修为调整+流派调整)
                zuanqian = int(info['人物加护估值']) + int(info['人物炼护估值']) + int(info['孩子加护估值'])
                info['最终估值'] =  str(max(zuanqian,int((zuanqian + (int(info['硬件估值总和'])-zuanqian)*(1+TiaozhengYinzi1)+int(info['软件估值总和']))*(1+TiaozhengYinzi2))))
#                info['最终估值'] = str(int(info['硬件估值总和'])*(float(info['修为调整因子'])+(float(info['装评调整因子'])-1)*0.5))
                info['市场调整金额'] = str(fun.ShichangTiaozheng(conn,info))
                #print(info)            
                ###写入数据库
                if cursor.execute("SELECT * FROM tx3 WHERE 藏宝阁编号="+info['藏宝阁编号']+" AND 服务器='"+info['服务器']+"' AND 更新时间>=DATE_SUB(CURDATE(),INTERVAL 30 DAY)"):
                    #如果角色已经在藏宝阁最近一个月的数据里存在，则更新价格，日期，修为调整因子和最终估值（修为调整因子和最终估值是根据现有行情变化的）
                    sql3 = 'UPDATE tx3 SET '
                    for x in info:
                        sql3 = sql3 + x + "='" + info[x] + "',"
                    sql3 = sql3[:-1] + " WHERE 藏宝阁编号='"+info['藏宝阁编号']+"' AND 服务器='"+info['服务器']+"'"   
                    cursor.execute(sql3)               
                    #cursor.execute("UPDATE tx3 SET 价格="+info['价格']+",更新时间='"+info['更新时间']+"',修为调整因子="+info['修为调整因子']+",装评调整因子="+info['装评调整因子']+",门派调整因子="+info['门派调整因子']+",特殊属性调整因子="+info['特殊属性调整因子']+",最终估值="+info['最终估值']+" WHERE 藏宝阁编号="+info['藏宝阁编号']+" AND 服务器='"+info['服务器']+"'")   
                    #cursor.execute("UPDATE tx3 SET 价格=%s,更新时间=%s,修为调整因子=%s,装评调整因子=%s,门派调整因子=%s,最终估值=%s WHERE 藏宝阁编号=%s AND 服务器=%s",(info['价格'],info['更新时间'],info['修为调整因子'],info['装评调整因子'],info['门派调整因子'],info['最终估值'],info['藏宝阁编号'],info['服务器']))
                else:
                    sql1 = ",".join(info.keys())
                    sql2 = ""
                    for x in info:
                        sql2 = sql2 + "'" + info[x] + "',"
                    #cursor.execute("INSERT INTO tx3(藏宝阁编号,服务器,角色名称,门派,性别,等级,神启境界,修为,装评,加护,炼护,价格,生命,物防,法防,知彼,回避,神明,最大物攻,最大法攻,最小物攻,最小法攻,附伤,命中,会心,重击,追电,骤雨,疾语,人祸,万钧,铁壁,诛心,御心,王朝军资,天域声望,启慧等级,天灵点数,特殊元魂珠,孩子资质,VIP9,防护特技,特殊时装)VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}','{37}','{38}','{39}','{40}','{41}','{42}');".format(info['藏宝阁编号'],info['服务器'],info['角色名称'],info['门派'],info['性别'],info['等级'],info['神启境界'],info['修为'],info['装评'],info['加护'],info['炼护'],info['价格'],info['生命'],info['物防'],info['法防'],info['知彼'],info['回避'],info['神明'],info['最大物攻'],info['最大法攻'],info['最小物攻'],info['最小法攻'],info['附伤'],info['命中'],info['会心'],info['重击'],info['追电'],info['骤雨'],info['疾语'],info['人祸'],info['万钧'],info['铁壁'],info['诛心'],info['御心'],info['王朝军资'],info['天域声望'],info['启慧等级'],info['天灵点数'],info['特殊元魂珠'],info['孩子资质'],info['VIP9'],info['防护特技'],info['特殊时装']))
                    #上面的execute也可以正常执行，但是太长了而且不易于维护，简化一下
                    #print("INSERT INTO tx3("+sql1+") VALUES("+sql2[:-1]+")")
                    cursor.execute("INSERT INTO tx3("+sql1+") VALUES("+sql2[:-1]+")")
            conn.commit()  #commit可以放在这里提交整页数据，而不必每个角色提交一次
            time.sleep(random.randint(1,2))     #增加随机延时,避免被服务器盯上
            print('第'+str(page)+'页加载+计算耗时：'+str(time.time()-startTime))
            logging.info('第'+str(page)+'页加载+计算耗时：'+str(time.time()-startTime))
    cursor.close()
    conn.close()     
    
#######主进程开始#######
startTimeTotal = time.time()
logging.basicConfig(filename='tx3CBG.log', filemode="a",level=logging.INFO,format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

global header,url
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer' : 'https://tx3.cbg.163.com/cgi-bin/equipquery.py?act=show_overall_search'
    }

###获取总页数
url = 'https://tx3.cbg.163.com/cgi-bin/search.py?act=overall_search_role&order_by=&other_arg=&price_min=50000'
#url = 'https://tx3.cbg.163.com/cgi-bin/search.py?act=overall_search_role&order_by=&page=1&other_arg=&xiuwei_min=66581&xiuwei_max=66581&'
PageData = requests.get(url,headers = header)
if PageData.status_code == 200:
    PageData.encoding = 'gb2312'
    PageDataJson = json.loads(PageData.text)
    TotalPage = PageDataJson['paging']['total_pages']
print("总页数" + str(TotalPage))

###写入数据库(单线程)  ！！！CBG最多只显示100页，单线程足以满足！！！
pageList = list(range(1,101))
pageList.reverse()   #倒序不会遗漏
catchRole(pageList)

##写入数据库(三线程)
#pages = [range(1,21),range(21,41),range(41,61)]
#threads = []
#for page in pages:
#    thread = threading.Thread(target=catchRole,args=(page,))
#    threads.append(thread)
#for t in threads:
#    t.start()  #启动每个线程
#for t in threads:
#    t.join()  #等待每个线程执行结束

endTimeToal = time.time()
print('总耗时'+str(endTimeToal-startTimeTotal)+'s')
logging.info('总耗时'+str(endTimeToal-startTimeTotal)+'s')