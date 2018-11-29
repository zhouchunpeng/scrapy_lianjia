# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from urllib import parse
from scrapy.loader import ItemLoader
from LianJia.items import chengjiaoitem
from urllib import parse
from scrapy import signals
# 之后可以做Q房网的成交

class ChengjiaoSpider(scrapy.Spider):
    name = 'chengjiao'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sh.lianjia.com/chengjiao/beicai/']

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    max_page = 2

    def parse(self, response):
        # 爬取具体每一页的html
        post_nodes = response.css('.listContent li a[href$=".html"]')
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
            url_sub_detail = parse.urljoin(response.url, url_sub)
            for page in range(self.max_page):
                url_page = parse.urljoin(response.url, url_sub_detail) + 'pg' + str(page)
                yield Request(url=url_page, callback=self.parse)

    def parse_detail(self,response):
        # 链接itmes
        cj_item = chengjiaoitem()

        # 通过css选择器提取字段
        data_base = response.css('.base .content li::text').extract() #基础属性

        area = data_base[2].rstrip()  # 面积

        usage_type = response.css('.transaction .content li:nth-child(4)::text').extract()[0].rstrip() # 房屋用途

        building_time = data_base[7].rstrip() # 建筑年代
        direction = data_base[6].rstrip()  # 朝向
        elevator = data_base[13].rstrip()   # 电梯
        floor = data_base[1].rstrip()  # 楼层

        district = response.css('.deal-bread a[href*="chengjiao"]::text').extract()[1][0:2]  # 区
        sub_district = response.css('.deal-bread a[href*="chengjiao"]::text').extract()[2][0:2]  # 镇/街道办
        it_name =  response.css('.house-title .wrapper h1::text').extract()[0].split()[0].rstrip()  # 小区名字
        # it_name = response.css('.house-title .wrapper::text').extract()[0].split()[0]


        quality = data_base[8].rstrip() # 装修与否
        shape = data_base[0].rstrip() # 户型

        total_price = response.css('.price .dealTotalPrice i::text').extract()[0] # 总价
        unit_price = response.css('.price b::text').extract()[0]# 单价

        data_msg = response.css('.msg label::text').extract()
        list_price= data_msg[0]# 挂牌价格

        discount_times= data_msg[2]  # 调价次数
        match_dt = re.match(".*?(\d+).*", discount_times)
        if match_dt:
            discount_times= int(match_dt.group(1))
        else:
            discount_times= 0

        deal_date = response.css('.house-title .wrapper span::text').extract()[0].split()[0] # 成交日期

        deal_period = data_msg[1]  # 成交周期
        match_dp = re.match(".*?(\d+).*", deal_period)
        if match_dp:
            deal_period = int(match_dp.group(1))
        else:
            deal_period = 0

        field_visit = data_msg[3] # 带看次数
        match_visit = re.match(".*?(\d+).*", field_visit)
        if match_visit:
            field_visit = int(match_visit.group(1))
        else:
            field_visit = 0

        follow = data_msg[4] # 关注人数
        match_follow = re.match(".*?(\d+).*", follow)
        if match_follow:
            follow = int(match_follow.group(1))
        else:
            follow = 0

        views = data_msg[5] # 浏览情况
        match_view = re.match(".*?(\d+).*", views)
        if match_view:
            views = int(match_view.group(1))
        else:
            views = 0

        # 链接
        link = response.url # 链接
        cj_item['area'] = area
        cj_item['usage_type'] = usage_type
        cj_item['building_time'] = building_time
        cj_item['direction'] = direction
        cj_item['elevator'] = elevator
        cj_item['floor'] = floor
        cj_item['district'] = district
        cj_item['sub_district'] = sub_district
        cj_item['it_name'] = it_name
        cj_item['quality'] = quality
        cj_item['shape'] = shape
        cj_item['total_price'] = total_price
        cj_item['unit_price'] = unit_price
        cj_item['list_price'] = list_price
        cj_item['discount_times'] = discount_times
        cj_item['deal_date'] = deal_date
        cj_item['deal_period'] = deal_period
        cj_item['field_visit'] = field_visit
        cj_item['follow'] = follow
        cj_item['views'] = views
        cj_item['link'] = link
        yield cj_item
