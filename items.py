# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# https://doc.scrapy.org/en/latest/topics/items.html
# See documentation in:

import scrapy

class chengjiaoitem(scrapy.Item):
    # define the fields for your item here like:
    # time = scrapy.Field() # 记录时间
    area = scrapy.Field() # 面积
    usage_type = scrapy.Field()  # 房屋用途
    building_time = scrapy.Field() #建筑年代
    direction = scrapy.Field() # 朝向
    elevator = scrapy.Field() # 电梯
    floor = scrapy.Field() # 楼层
    district = scrapy.Field() # 区
    sub_district = scrapy.Field() #镇/街道办
    it_name = scrapy.Field() #小区名字
    quality = scrapy.Field() #装修与否
    shape = scrapy.Field() #户型
    total_price = scrapy.Field() #总价
    unit_price = scrapy.Field()  # 单价
    list_price = scrapy.Field() #挂牌价格
    discount_times = scrapy.Field() #调价次数
    deal_date = scrapy.Field() #成交日期
    deal_period = scrapy.Field() #成交周期
    field_visit = scrapy.Field()  #带看次数
    follow = scrapy.Field() #关注人数
    views = scrapy.Field() #浏览情况
    link = scrapy.Field()#链接
    # deal_hist = scrapy.Field()  # 历史成交记录

    def get_insert_sql(self):
        insert_sql = """
            insert into chengjiaoLj1(area, usage_type,building_time, direction, elevator, 
                                    floor, district, sub_district,it_name,quality, 
                                    shape, total_price, unit_price, list_price,discount_times,
                                    deal_date,deal_period,field_visit,follow,views,link)
            VALUES (%s, %s, %s, %s, %s,
                    %s,%s, %s, %s, %s,
                    %s, %s,%s, %s, %s,
                    %s, %s, %s, %s, %s,%s)  
        """
        params = (self["area"], self["usage_type"],self["building_time"], self["direction"],self["elevator"],
                  self["floor"],self["district"], self["sub_district"],self["it_name"],self["quality"],
                  self["shape"], self["total_price"], self["unit_price"],self["list_price"],self["discount_times"],
                  self["deal_date"],self["deal_period"],self["field_visit"],self["follow"],self["views"],self["link"])

        return insert_sql, params


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    monitor_time = scrapy.Field()
    area = scrapy.Field()
    building_time = scrapy.Field()
    direction = scrapy.Field()
    elevator = scrapy.Field()

    floor = scrapy.Field()
    # id = scrapy.Field()
    district = scrapy.Field()
    sub_district = scrapy.Field()
    it_name = scrapy.Field()

    quality = scrapy.Field()
    shape = scrapy.Field()
    # title = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    sale_date = scrapy.Field()
    trade_year = scrapy.Field()
    zjjy = scrapy.Field()
    fcsx = scrapy.Field()
    tag = scrapy.Field()
    link = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into esflianjia(monitor_time, area, building_time, direction, elevator,
                                    floor, district, sub_district,it_name, quality, 
                                    shape, total_price, unit_price, sale_date,trade_year,
                                    zjjy, fcsx,tag,link)
                                    
            VALUES (%s, %s, %s, %s, %s,
                     %s, %s, %s, %s,%s,
                     %s, %s, %s, %s, %s,
                      %s,%s, %s,%s)  
        """
        params = (self["monitor_time"], self["area"], self["building_time"], self["direction"], self["elevator"],
                  self["floor"], self["district"], self["sub_district"], self["it_name"], self["quality"],
                  self["shape"], self["total_price"], self["unit_price"], self["sale_date"], self["trade_year"],
                  self["zjjy"],self["fcsx"],self["tag"],self["link"])


        return insert_sql, params