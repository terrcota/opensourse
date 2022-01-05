import requests  # 数据请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块 第三方模块 pip install parsel
import re  # 正则表达式模块
import csv  # csv数据保存
import pymongo

client = pymongo.MongoClient('localhost', 27017)
spider = client['spider_data']
collection = spider['spiderData']
f = spider['num']
f2 = spider['average']
f3 = spider['average_m']
f4 = spider['elevator']
f5 = spider['furnish']

shiqu = ['开发区', '沙河口', '高新园区', '金州', '甘井子', '普兰店', '旅顺口', '中山', '瓦房店', '西岗']
dianti = ['有电梯', '无电梯']
zhuangxiu = ['精装', '简装', '毛坯', '其他']

for i in shiqu:
    counts = collection.find({'市区': i})
    print(i)
    num = 0
    cost = 0
    cost_m = 0
    for count in counts:
        num = num + 1
        tx = float(count['价格(万元)'])
        ty = float(count['面积(㎡)'])
        tz = tx / ty
    #   print(tx)
    #   print(ty)
        cost = cost + tx
        cost_m = cost_m + tz
#二手房分布数量
    dit = {
        '市区': i,
        '数量': num
    }
    f.insert_one(dit)
    print(num)

#二手房平均价格
    avg = cost / num
    avg2 = round(avg , 2)
    dita = {
        '市区': i,
        '平均价格': avg2
    }
    f2.insert_one(dita)
    print(avg2)

#二手房一平平均价格
    avg_m = cost_m / num
    avg_m2 = round(avg_m , 2)
    dita_m = {
        '市区': i,
        '平均价格': avg_m2
    }
    f3.insert_one(dita_m)
    print(avg_m2)

#二手房电梯情况
    ditd = {
        '市区': i,
    }
    for j in dianti:
        k = 0
        countd = collection.find({'市区': i, '电梯': j})
        for count in countd:
            k = k + 1
        ditd[j] = k
    f4.insert_one(ditd)

#二手房装修情况
    ditz = {
        '市区': i,
    }
    for j in zhuangxiu:
        k = 0
        countz = collection.find({'市区': i, '装修情况': j})
        for count in countz:
            k = k + 1
        ditz[j] = k
    f5.insert_one(ditz)
