# -*- coding: utf-8 -*-
# Author    : wangweipeng
# @time     : 2019/3/4 16:05
# @fILE     : selenlum.py
# @Software : PyCharm
# modify    :2019/3/5 8:30 by wangweipeng
# 修改内容  : 加入try判断"Message: Reached error page"网络异常后继续执行。
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import requests
driver = webdriver.Firefox()
#获取首页上的数据
url = "https://www.mzitu.com/xinggan"
# 使用BS4获取页面的HTML
code = driver.get(url)
bsp = BeautifulSoup(driver.page_source, 'html.parser')
span = bsp.select('#pins span a')
# 获取页数
num = int(bsp.select('.nav-links a')[-2].get_text())
n=1
for n in range(1,num):
    urlnew = "https://www.mzitu.com/xinggan/page/{pages}/"
    urls = urlnew.format(pages=n)
    code = driver.get(urls)
    bsp = BeautifulSoup(driver.page_source, 'html.parser')
    span = bsp.select('#pins span a')
    for i in span:
        # 获取详情页的网页和主题，便于后续存放。
        html = i.get('href')
        title = i.get_text()
        # 开始爬取详情页
        # 使用BS4获取页面的HTML
        codexiangqing = driver.get(html)
        bspxiangqing = BeautifulSoup(driver.page_source, 'html.parser')
        spanxiangqing = bspxiangqing.select('.main-image a img')[0].get('src')
        # 获取详情页面的页数
        numbs = int(bspxiangqing.select('.pagenavi a')[-2].get_text())
        j = 1
        # 开始下载图片
        if ": " in title:
            title = title.replace(': ', ' ')
        print(n)
        if not os.path.exists(title):
            os.mkdir(title)
            print('开始下载图片', title)
            for j in range(1, numbs):
            #
                try:
                    htmls = html + '/' + str(j)
                    codexiangqingnew = driver.get(htmls)
                    bspxiangqingnew = BeautifulSoup(driver.page_source, 'html.parser')
                    spanxiangqingnew = bspxiangqingnew.select('.main-image a img')[0].get('src')

                    # 存放到对应文件夹中
                    filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), title, title + str(j))
                    headers = {
                        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
                        'Referer': 'http://www.mzitu.com/xinggan/'
                    }
                    response = requests.get(spanxiangqingnew, headers=headers)
                    with open(filename, 'wb') as img:
                        img.write(response.content)
                except:
                    continue
                j = j + 1
    n = n+1
print('====================The end================')
