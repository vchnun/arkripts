import requests
from lxml import etree
from bs4 import BeautifulSoup  
import csv
import os

url ='http://ak.mooncell.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88'
headers = {'User-Agent': 'my custom user agent', 'Cookie': 'haha'}
r = requests.get(url, headers=headers)

# s = etree.HTML(r.text)
# a0 = s.xpath('//*[@id=""mw-content-text"]/tr[2]')

#使用自带的html.parser解析，速度慢但通用
soup = BeautifulSoup(r.text, "html.parser")#.prettify()
#或者soup = BeautifulSoup(html, "html5lib")

#按照CSS类名搜索tag的功能非常实用,但标识CSS类名的关键字 class 在Python中是保留字,使用 class 做参数会导致语法错误.从Beautiful Soup的4.1.1版本开始,可以通过 class_ 参数搜索有指定CSS类名的tag
#查找dl标签class为dataItem02的所有dl标签
agentList = []
for tag in soup.find_all("div", class_="smwdata"):
    agentList.append(tag.attrs) # 保留属性

headers = agentList[0].keys()
if os.path.exists('rawdata.csv'):
    os.remove('rawdata.bak.csv')
    os.rename('rawdata.csv', 'rawdata.bak.csv')
with open('./data/rawdata.csv','w',newline='', encoding='utf-8')as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(agentList)

headers = ['代号', '稀有度', '职业', '位置', '标签',]
keys = ['data-cn', 'data-rarity', 'data-class', 'data-position', 'data-tag',]
f = open('./data/hrdata.csv','w',newline='', encoding='utf-8')
f_csv = csv.writer(f)
f_csv.writerow(headers)
for agent in agentList:
    if '公开招募' in agent['data-approach']:
        f_csv.writerow([agent[key] for key in keys])
f.close()