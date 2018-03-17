#!/usr/bin/python
# -*- coding: utf-8 -*-
# 导入模块
import requests
import json
import datetime


# 生成时间列表
def dat_tim(stardate="2014-01-01"):
    # 起始日期
    day_star = datetime.datetime.strptime(stardate, "%Y-%m-%d").date()
    # 每次增加变更天数，1天
    add_day_one = datetime.timedelta(days=1)
    # 现在的日期
    now_date =datetime.datetime.now().date()
    # 起始日期到现在几天
    delta_day = now_date-day_star
    delta_day = delta_day.days
    # 生成事件列表 每次加1天
    date_data = list()
    for i in range(delta_day):
        add_date = day_star.strftime("%Y%m%d")
        date_data.append(add_date)
        day_star = day_star + add_day_one
    return(date_data)


# 获取从起始日期到现在的日期列表
date_list = dat_tim()

# 制作获取地址 https://developer.am.mufg.jp/fund_information_all_date/base_date/{val1}
# 例如/base_date/20170915
url = "https://developer.am.mufg.jp/fund_information_all_date/base_date/" + str(20150515)
r = requests.get(url)
#print(r.text)
#print(r.status_code)
#print(r.raise_for_status())
c = r.json()['value']
print(len(c))
