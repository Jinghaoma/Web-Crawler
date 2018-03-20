#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from threading import Thread,Lock
import os
import time
import pandas as pd

# 基金代码
code = 340001
target_url = "http://fund.eastmoney.com/f10/jjjz_"+str(code)+".html"


def initspider(url=target_url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)  # 要抓取的网页地址

    # 找到"下一页"按钮,就可以得到它前面的一个label,就是总页数
    getpage_text = driver.find_element_by_id("pagebar").find_element_by_xpath(
        "div[@class='pagebtns']/label[text()='下一页']/preceding-sibling::label[1]").get_attribute("innerHTML")
    # 得到总共有多少页
    total_page = int("".join(filter(str.isdigit, getpage_text)))
    # 返回
    return driver, total_page


def getdata(myrange, driver, lock):
    for x in myrange:
        # 锁住
        lock.acquire()

        tonum = driver.find_element_by_id("pagebar").find_element_by_xpath(
            "div[@class='pagebtns']/input[@class='pnum']")  # 得到 页码文本框
        jumpbtn = driver.find_element_by_id("pagebar").find_element_by_xpath(
            "div[@class='pagebtns']/input[@class='pgo']")  # 跳转到按钮

        tonum.clear()  # 第x页 输入框
        tonum.send_keys(str(x))  # 去第x页
        jumpbtn.click()  # 点击按钮

        # 抓取
        WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/label[@value={0} and @class='cur']".format(x)) != None)

        #with open("data/{0}.txt".format(x), 'wb') as f:
        #    f.write(driver.find_element_by_id("jztable").get_attribute("innerHTML").encode('utf-8'))
        #    f.close()
        # 保存到项目中
        c = driver.find_element_by_id("jztable").text
        d = BeautifulSoup(c, "lxml").text
        d = d.replace("\n", "\r\n")
        with open("data/{0}.txt".format(x), 'wb') as f:
           f.write(d.encode("utf-8"))
           f.close()

        # 解锁
        lock.release()


# 第1页数据无法加载完，这个函数重新抓取第页数据
def getdata1(driver, lock):
    x = 1
    # 锁住
    lock.acquire()

    tonum = driver.find_element_by_id("pagebar").find_element_by_xpath(
        "div[@class='pagebtns']/input[@class='pnum']")  # 得到 页码文本框
    jumpbtn = driver.find_element_by_id("pagebar").find_element_by_xpath(
        "div[@class='pagebtns']/input[@class='pgo']")  # 跳转到按钮

    tonum.clear()  # 第x页 输入框
    tonum.send_keys(str(x))  # 去第x页
    jumpbtn.click()  # 点击按钮
    time.sleep(5)

    # 抓取
    WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id("pagebar").find_element_by_xpath(
        "div[@class='pagebtns']/label[@value={0} and @class='cur']".format(x)) != None)

    c = driver.find_element_by_id("jztable").text
    d = BeautifulSoup(c, "lxml").text
    d = d.replace("\n", "\r\n")
    with open("data/{0}.txt".format(x), 'wb') as f:
        f.write(d.encode("utf-8"))
        f.close()

    # 解锁
    lock.release()


# 开始抓取函数
def beginspider():
    # 初始化爬虫
    (driver, total_page) = initspider()
    # 创建锁
    lock = Lock()

    r = range(1, int(total_page)+1)
    step = 10
    range_list = [r[x:x + step] for x in range(0, len(r), step)]  # 把页码分段
    thread_list = []
    for r in range_list:
        t = Thread(target=getdata, args=(r, driver, lock))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()  # 这一步是需要的,等待线程全部执行完成
    getdata1(driver,lock)

    print("抓取完成")
    return total_page
# #################上面代码就完成了 抓取远程网站html内容并保存到项目中的 过程


def save_data(page):
    # 获取目录下文件名
    f_name = list()
    for i in range(1, page+1):
        f_name.append(str(i)+".txt")
    dat_all = pd.DataFrame(columns=["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态", "分红送配"])
    for name in f_name:
        dat = pd.read_csv("data/"+name, encoding="utf-8",sep = " ")
        dat_all = pd.concat([dat_all, dat])
        os.remove("data/"+name)
    file_name = "data/"+str(code)+"_all_data.csv"
    dat_all.to_csv(file_name, index=False, encoding="utf-8")


total_page = beginspider()
save_data(total_page)

# a = pd.read_csv("data/164906_all_data.csv")
# a = a.sort_index(ascending=False)
# a.to_csv("data/164906_all_data.csv", index=False, encoding="utf-8")
# a
