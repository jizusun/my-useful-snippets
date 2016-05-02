# -*- coding: utf-8 -*-

import requests
from lxml import html
import json
import re

# 用于保存每一期刊物的元数据
journals = []
# 用于跟网站子目录拼接
base_url = "http://qhzk.lib.tsinghua.edu.cn:8080"

# 用于获取每一期的刊名和链接
def get_toc():
    toc_page = base_url + "/Tsinghua_Journal/year.html"
    response = requests.get(toc_page)
    # 默认编码为ISO-8859-1，此处将编码修正为UTF-8
    # https://github.com/kennethreitz/requests/issues/1604
    response.encoding = 'utf-8'
    doc = html.fromstring(response.text)

    for link in doc.xpath('//table//a'):
        url = link.get('href')
        description = link.text
        if(url):
            one_journal = {
                    'title': description,
                    'link': base_url + url, 
                    }
            print one_journal['title'],one_journal['link']
            journals.append(one_journal)

def get_page_count():
    for journal in journals: 
        response = requests.get(journal['link'])
        doc = html.fromstring(response.text)
        page_count = doc.xpath('//div[@class="command-bar"]/a[last()]/@href')[0]
        # page_count的格式如 'javascript:gotoPage(17)'
        page_count = re.search(r'\d+', page_count)
        page_count = page_count.group()
        journal['page_count'] = page_count
        print json.dumps(journal, ensure_ascii=False).encode('utf8')

def get_page_in_range(start, count):
    # start: 1, count: 3

    for journal in journals[:3]: 
        for page_no in range(start, start+count):
            data = {
                    'action': 'image',
                    'jumpPage': page_no,
                   }
            turnpage_response = requests.post(journal['link'], data=data)
            print turnpage_response.url
            showimage_payload = {
                    'rand': 'aaa'
                    }
            showimage_url = journal['link'].replace('turnPage', 'showImage')
            image_response = requests.get(showimage_url, params=showimage_payload)
            print image_response.url
            dirname = '/home/sunjizu/Documents/python-dev-env/tsinghua_downloads/'
            filename = u'%s-第%d页.png' % (journal['title'], page_no)
            with open(dirname+filename, 'wb') as f:
                f.write(image_response.content)
                print '%s saved' % filename
        
       # print json.dumps(journal, ensure_ascii=False).encode('utf8')


def save_to_file():
    with open('toc.txt', 'w') as f:
        json_string = json.dumps(journals, ensure_ascii=False).encode('utf8')
        f.write(json_string)
    # xpath to get the end page number:
    # '//div[@class="command-bar"]/a[last()]/@href'


if __name__ == '__main__':
    get_toc()
    # get_page_count()
    get_page_in_range(1, 3)
