import requests  # 数据请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块 第三方模块 pip install parsel
import re  # 正则表达式模块
import csv  # csv数据保存
import pymongo

client = pymongo.MongoClient('localhost', 27017)
spider = client['spider_data']
spiderData = spider['spiderData']

for page in range(1, 101):
    # 1. 发送请求, 是对于房源列表页发送请求33
    print(f'正在爬取第{page}页的数据内容')
    print('正在爬取第%s页的数据内容' % page)
    url = f'https://dl.lianjia.com/ershoufang/pg{page}/'
    # 请求头: 把python代码进行伪装 成浏览器 对于服务器发送请求 模拟浏览器发送请求
    # User-Agent: 浏览器的基本标识
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    # 使用requests这个模块里面get方法 对于 url地址发送请求 并且携带上headers请求头
    response = requests.get(url=url, headers=headers)
    # <Response [200]>  响应体对象 200 状态码 表示请求成功
    # 2. 获取数据 获取响应体的文本数据
    # print(response.text) # 获取response.text html字符串数据内容
    # 3. 解析数据, 提取我们想要的内容, 房源详情页url
    # 你想要对于字符串数据内容 直接进行解析提取, 只能用re正则表达式
    selector = parsel.Selector(response.text)
    # css选择器, 解析方法 就是 根据标签属性内容 提取相关的数据
    href = selector.css('li.clear a.noresultRecommend::attr(href)').getall()
    for index in href:
        #  4. 发送请求, 对于房源详情页url地址发送请求
        response_1 = requests.get(url=index, headers=headers)
        # 5. 获取数据
        # 6. 解析数据, 提取房源基本信息 售价 标题 单价 面积 户型....
        selector_1 = parsel.Selector(response_1.text)
        # # 标题
        # title = selector_1.css('div.title .main::text').get()
        # # 售价
        # price = selector_1.css('.price .total::text').get() + '万元'
        # print(title, price)
        area = selector_1.css('.areaName .info a:nth-child(1)::text').get()  # 区域
        community_name = selector_1.css('.communityName .info::text').get()  # 小区
        room = selector_1.css('.room .mainInfo::text').get()  # 户型
        room_type = selector_1.css('.type .mainInfo::text').get()  # 朝向
        height = selector_1.css('.room .subInfo::text').get()  # 楼层
        height = re.findall('共(\d+)层', height)[0]
        sub_info = selector_1.css('.type .subInfo::text').get().split('/')[-1]  # 装修
        Elevator = selector_1.css('.content li:nth-child(12)::text').get() + '电梯'  # 电梯
        if Elevator == '暂无数据电梯':
            Elevator = '无电梯'
        house_area = selector_1.css('.content li:nth-child(3)::text').get().replace('㎡', '')  # 面积
        price = selector_1.css('.price .total::text').get()  # 价格(万元)
        date = selector_1.css('.area .subInfo::text').get().replace('年建', '')  # 年份
        dit = {
            '市区': area,
            '小区': community_name,
            '户型': room,
            '朝向': room_type,
            '楼层': height,
            '装修情况': sub_info,
            '电梯': Elevator,
            '面积(㎡)': house_area,
            '价格(万元)': price,
            '年份': date,
            '详情页': index,
        }
        #csv_writer.writerow(dit)

        spiderData.insert_one(dit)
        print(area, community_name, room, room_type, height, sub_info, Elevator, house_area, price, date, index,
              sep='|')