import radar
import requests
import json
from lxml import etree
import random
import re

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

       ]

url_list = ["https://news.sina.com.cn/w/2022-07-08/doc-imizirav2530099.shtml",
            "https://news.sina.com.cn/o/2022-07-10/doc-imizmscv0830248.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizmscv0861069.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizirav2681735.shtml",
            "https://finance.sina.com.cn/tech/2022-07-09/doc-imizmscv0799203.shtml",
            "https://finance.sina.com.cn/china/2022-07-08/doc-imizmscv0568703.shtml",
            "https://news.sina.com.cn/s/2022-07-08/doc-imizirav2504940.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizmscv0835902.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizmscv0841698.shtml",
            "https://sports.sina.com.cn/china/j/2022-07-08/doc-imizirav2535520.shtml",
            "https://sports.sina.com.cn/g/pl/2022-07-08/doc-imizirav2459313.shtml",
            "https://mil.news.sina.com.cn/2022-07-07/doc-imizmscv0476837.shtml",
            "https://news.sina.com.cn/c/2022-07-09/doc-imizirav2663200.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizirav2688933.shtml",
            "https://news.sina.com.cn/w/2022-07-10/doc-imizirav2688483.shtml",
            "https://mil.news.sina.com.cn/2022-07-08/doc-imizmscv0659975.shtml",
            "https://mil.news.sina.com.cn/2022-07-07/doc-imizmscv0486658.shtml",
            "https://sports.sina.com.cn/basketball/nba/2022-07-08/doc-imizirav2459640.shtml",
            "https://sports.sina.com.cn/basketball/nba/2022-07-09/doc-imizirav2579456.shtml",
            "https://sports.sina.com.cn/tennis/atp/2022-07-09/doc-imizirav2565724.shtml",
            "https://sports.sina.com.cn/others/badmin/2022-07-10/doc-imizmscv0896531.shtml",
            "https://sports.sina.com.cn/basketball/nba/2022-07-10/doc-imizmscv0865974.shtml",
            "https://news.sina.com.cn/s/2022-07-10/doc-imizirav2701011.shtml",
            "https://news.sina.com.cn/c/2022-07-10/doc-imizmscv0902619.shtml"]
#线爬取网页内容在进行分类
xpath_list=[    "//div[@class='View']/ul[@class='list_14 list-0427']//li/a/@href",
                "//div[@class='rc-context read-context']//a/@href",
                "//div[@class='new-media-lab']//a/@href"
                ]
#headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
headers = {}
def crawl(url):   #获取网页响应，得到网页源码，以字符串形式返回
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url,headers = headers)
    data = response.content
    str1 = str(data,encoding='utf-8')
    return str1

def writetxt(datastr):  #只需要写入两列数据，一列是title，另外一列是url
    filename='D:\\t2.txt'
    with open(filename,'a',encoding='utf-8') as f:
        f.write(datastr+'\n')
    f.close()


def addurl(str):   #如果里面缺http服务，则加上
        if('http'not in str):
            if('javascript' in str):
                return
            str='https:'+str
        if('shtml' in str):
            url_list.append(str)


def crawl_page():
    count =0
    title_xpath = "//h1[@class='main-title']/text()"  # 当前页面的题目定位和url定位
    url_xpath = "//meta[@property='og:url']/@content"
    for i in url_list:
        str1 = crawl(i)
    # 以下是对第一个网页里面的进行，title和 url的爬取
        html = etree.HTML(str1)
        for url_item in xpath_list:
            url = html.xpath(url_item)
            for kitem in url:
                addurl(kitem)

        title_list = html.xpath(title_xpath)

        urls_list = html.xpath(url_xpath)
        if(len(title_list)==0 or len(urls_list)==0):
            continue
        print(title_list)
        print(urls_list)
        print("____________________________________________________\n")
        #访问时间\t用户ID\t[查询词]\t该URL在返回结果中的排名\t用户点击的顺序号\t用户点击的URL
        # 时间 用户id   title  url返回排名  用户点击序号   url
        strid=str(random.randint(00000000,99999999))+str(random.randint(00000000,99999999))
        str2 = radar.random_time().strftime('%H:%M:%S')+','+strid+','+'[' + title_list[0] + ']' + ','+str(random.randint(1,400))+',' +str(random.randint(1,79))+','+ urls_list[0]

        print(str2)
        writetxt(str2)
        count=count+1
        print(count)
        str2 = ''

if __name__ == '__main__':
    crawl_page()
