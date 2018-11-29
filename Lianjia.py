# -*- coding: utf-8 -*-
# 将中原地产、我爱我家、Q房网数据整合
import scrapy
import re
import datetime
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from urllib import parse
from scrapy.loader import ItemLoader
from LianJia.items import  LianjiaItem
from urllib import parse
from scrapy import signals

class LianjiaSpider(scrapy.Spider):
    name = 'Lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sh.lianjia.com/ershoufang/pudong/beicai']  #url可能是/beicai

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)


    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    max_page = 101

    def parse(self, response):
        # 爬取具体每一页的html
        post_nodes = response.css('.sellListContent li a[href$=".html"]')
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)


        # 获取链家网上所有的区域url
        url_list_distrcit = response.xpath('//div[@data-role ="ershoufang"]/div[1]/a/@href').extract()
        for url_district in url_list_distrcit:
            url_dis = parse.urljoin(response.url, url_district)
            yield Request(url=url_dis, callback=self.parse)

        # 获取链家网上所有的子区域的url
        # url_sub = response.css('.position dl:nth-child(2) div[data-role="ershoufang"] div:nth-child(2) a::attr(href)').extract()
        url_sub_list = response.css('div[data-role="ershoufang"] div:nth-child(2) a::attr(href)').extract()
        for url_sub in url_sub_list:
            url_sub_detail  = parse.urljoin(response.url, url_sub)
            for page in range(self.max_page):
                url_page = parse.urljoin(response.url, url_sub_detail) + 'pg' + str(page)
                yield Request(url=url_page,callback=self.parse)


    def parse_detail(self, response):
        esf_item = LianjiaItem()
        monitor_time = datetime.date.today().strftime('%Y-%m-%d') # today
        # 通过css选择器提取字段

        building_info = response.css('.area ::text').extract()
        # area = building_info[0] # 面积
        area = re.match('(\d*|\d*\.\d*)平米', building_info[0]).group(1)
        building_time = building_info[1] # 建设年代
        # building_time = re.match('(\d*)\w*', building_info[1]).group(1)
        match_bt = re.match('(\d*)\w*', building_time)
        if match_bt:
            building_time = match_bt.group(1)
        else:
            building_time = "未知"
        data_base = response.css('.base .content li::text').extract()
        direction = response.css('.type .mainInfo::text').extract()[0] # 朝向
        if len(data_base) <10:
            elevator = "无"
        else:
            elevator = data_base[10]  # 电梯
        floor = data_base[1] # 楼层

        # id = response.css('.houseRecord .info::text').extract()[0] # 链家id号 可以不要了

        location_info = response.css('.areaName .info a::text').extract()
        district = location_info[0] # 区
        sub_district = location_info[1] # 镇/街道办

        it_name = response.css('.communityName a::text').extract_first() # 小区名称
        quality = data_base[8]  # 装修情况
        if quality not in  ["精装","简装","毛坯","其他"]:
            quality = data_base[6]

        shape = data_base[0] # 户型
        # title = response.css('.title h1::text').extract()[0] # 标题  可以不要了
        total_price = response.css('.price .total::text').extract()[0] # 总价
        if float(total_price)<8.0:
            total_price = str(10000*float(total_price))
        unit_price = response.css('.unitPrice .unitPriceValue::text').extract()[0] # 单价

        trasaction_info = response.css('.transaction .content li span::text').extract()
        sale_date =trasaction_info[1] # 挂牌时间
        zjjy =trasaction_info[5] # 上次交易时间
        trade_year = trasaction_info[9]  # 房屋交易年限
        fcsx = trasaction_info[3] # 房产属性
        tag = ','.join(response.css('.tags .content a::text').extract())
        link = response.url # 链接

        esf_item['monitor_time'] = monitor_time
        esf_item['area'] = area
        esf_item['building_time'] = building_time
        esf_item['direction'] = direction
        esf_item['elevator'] = elevator
        esf_item['floor'] = floor
        # esf_item['id'] = id
        esf_item['district'] = district
        esf_item['sub_district'] = sub_district
        esf_item['it_name'] = it_name
        esf_item['quality'] = quality
        esf_item['shape'] = shape
        # esf_item['title'] = title
        esf_item['total_price'] = total_price
        esf_item['unit_price'] = unit_price
        esf_item['sale_date'] = sale_date
        esf_item['trade_year'] = trade_year
        esf_item['zjjy'] = zjjy
        esf_item['fcsx'] = fcsx
        esf_item['tag'] = tag
        esf_item['link'] = link

        yield esf_item
