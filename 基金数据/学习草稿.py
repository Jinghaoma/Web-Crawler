#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://www.baidu.com/")
# 百度关键词输入框
searchInput = driver.find_element_by_id("kw")
# 我们来搜索一下 "python"这个关键字
searchInput.send_keys("python")
# 百度输入框提交按钮
searchSubmitBtn = driver.find_element_by_id("su")
searchSubmitBtn.submit()  # 模拟提交表单

# 因为百度的搜索是异步的
# 我们这里设置等待20秒
# 如果网页标题中包含了"python" 我们就认为加载成功了
WebDriverWait(driver,20).until(expected_conditions.title_contains("python"))

print(driver.title) # python_百度搜索
