###修改数据库
import pymysql
import function as fun
conn = pymysql.connect(host='localhost',port=3306,user='root',password='yhwj1234',db='zhilianzhaopin',charset='utf8')
cursor = conn.cursor()
#cursor.execute("SELECT * FROM tx3 WHERE 更新时间<=DATE_SUB(CURDATE(),INTERVAL 14 DAY) and 价格<1.5*最终估值 and 修为调整因子>0 and 装评调整因子>0 and 攻击调整因子>0 and 防御调整因子>0 and 金色属性调整因子>0 and 门派及流派调整>0")
cursor.execute("SELECT * FROM tx3")

sql = []
for j in cursor.fetchall():
    info = {}
    for i in range(0,len(cursor.description)):
        info[cursor.description[i][0]] = j[i]  
    info['综合防御'] = fun.GetFangyu(info)
    sql.append("UPDATE tx3 SET 综合防御="+str(info['综合防御'])+" WHERE 角色名称='"+info['角色名称']+"' AND 服务器='"+info['服务器']+"'")
    #print(info)
for x in sql:
    print(info['序号'])
    if cursor.execute(x) == 1:
        print(x)
        conn.commit()
cursor.close
conn.close
   

