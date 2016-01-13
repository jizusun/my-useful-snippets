# -*- coding: utf-8 -*-

import requests
from lxml import html
import json
import re

journals = []
base_url = "http://qhzk.lib.tsinghua.edu.cn:8080"

def get_toc():
    toc_page = base_url + "/Tsinghua_Journal/year.html"
    response = requests.get(toc_page)
    response.encoding = 'utf8'
    doc = html.fromstring(response.text)


    for link in doc.xpath('//table//a'):
        url = link.get('href')
        description = link.text
        if(url):
            one_journal = {
                    'title': description,
                    'link': base_url + url, 
                    }
            print one_journal['title']
            if one_journal['title'] == u'总第449期':
                break
            journals.append(one_journal)

def get_page_count():
    for journal in journals: 
        response = requests.get(journal['link'])
        doc = html.fromstring(response.text)
        page_count = doc.xpath('//div[@class="command-bar"]/a[last()]/@href')[0]
        # page_count: 'javascript:gotoPage(17)'
        page_count = re.search(r'\d+', page_count)
        page_count = page_count.group()
        journal['page_count'] = page_count
        print json.dumps(journal, ensure_ascii=False).encode('utf8')

def get_page_in_range(start, count):
    # start: 1, count: 3
    turnpage_url = base_url + "/Tsinghua_Journal/turnPage"
    showimage_url = base_url + '/Tsinghua_Journal/showImage'

    for journal in journals: 
        for page_no in range(start, start+count):
            data = {
                    'action': 'image',
                    'jumpPage': page_no,
                    }
            turnpage_response = requests.post(journal['link'], data=data)
            print turnpage_response.url
            showimage_payload = {
                    'totalvolume': journal['title'],
                    'pageno': page_no,
                    'rand': 'aaa'
                    }
            response = requests.get(showimage_url, params=showimage_payload)
            dirname = '/home/jizusun/testbed/mg/tsinghua_downloads/'
            filename = u'%s-第%d页.jpg' % (journal['title'], page_no)
            with open(dirname+filename, 'wb') as f:
                f.write(response.content)
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
    get_page_in_range(1, 3)

