#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import os


cookie = 'cnkiUserKey=cede63ae-9916-adc9-1078-aa09edc2a4ea; lzstat_uv=12679637752591645635|2234092; LID=; ASP.NET_SessionId=acqfwe22ep0qa1vaag1wh555; SID=009003'
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'
acc = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

# 用于跟网站子目录拼接
root_url = "http://tongji.cnki.net/kns55/Navi/"
index_url = root_url + "HomePage.aspx?id=N2013080059&name=YSIEN&floor=1"
# 创建文件夹
download_dir ='gdxx_kjtj_data'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

sess = requests.Session()

# 用于获取每一期的刊名和链接
def get_yearbook_urls():
    # 用于保存每一期刊物的元数据
    journals = []

    response = sess.get(index_url)
    # 默认编码为ISO-8859-1，此处将编码修正为UTF-8
    # https://github.com/kennethreitz/requests/issues/1604
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html5lib')

    for link in soup.select('.list_h a'):
        title = link.getText()
        url = link.get('href')
        if(url):
            one_journal = {
                    'title': title,
                    'link': root_url + url, 
                    }
            journals.append(one_journal)
            print one_journal['title'],one_journal['link']
    return journals


def get_parts_in_year(year_url):
    r = sess.get(year_url)
    soup = BeautifulSoup(r.text, 'html5lib')

    year_info = []
    for part in soup.select('.TreeList a'):
        part_info = {}
        # GetChildCatalog('N2013080059', '002', '0', 'A_N2013080059000002')"
        params =  re.findall("'(.+?)'", part.get('onclick'))
        params = list(params)
        part_info['params'] = {
                'id': params[0],
                'code': params[1]+"?",
                'type': params[2],
                'fileid': params[3]
                }
        part_info['text'] = part.getText()
        year_info.append(part_info)
    return year_info

def get_files_in_part(part):
    get_child_category_url = 'http://tongji.cnki.net/kns55/Navi/GetChildCatalog.aspx'
    response = sess.post(get_child_category_url, data=part['params'])
    soup = BeautifulSoup(response.text, 'html5lib')
    files = []
    for row in soup.select('.dhmltable tr')[1:]:
        file = {}
        tds = row.select('td')
        file_links = tds[0].select('a')
        if len(file_links) == 1:
            file['file_name'] = tds[1].a.getText().strip() + '.pdf'
            file['file_name'] = file['file_name'].replace(' ', '_')
            file['link'] =  "http://tongji.cnki.net/kns55/" + tds[0].a.get('href')[3:] + 'pdf&dflag=pdfdown'
        else:
            file['file_name'] = tds[1].a.getText().strip() + '.xls'
            file['file_name'] = file['file_name'].replace(' ', '_')
            file['link'] = "http://tongji.cnki.net/kns55/" + tds[0].select('a')[1].get('href')[3:]
        files.append(file)
    return files

def get_pages_in_range(year_limit=None):
    years = get_yearbook_urls()
    # 遍历限定范围内的每一年
    for year in years[:year_limit]: 
        # 创建年份文件夹
        year_dir = os.path.join(download_dir, year['title'])
        if not os.path.exists(year_dir):
            os.makedirs(year_dir)
        parts = get_parts_in_year(year['link'])
        print year['title'], parts
        # 遍历这一年的每一部分
        # 为了测试先看第一部分
        #for part in parts[1:2]:
        for part in parts:
            # 创建该部分的文件夹
            part_dir = os.path.join(year_dir, part['text']) 
            print u'创建文件夹：' + part_dir
            if not os.path.exists(part_dir):
                os.makedirs(part_dir)
            files = get_files_in_part(part)
            sess.headers.update({'Referer': year['link'], 'Cookie': cookie, 'User-Agent': ua, 'Accept': acc})
            for file in files:
                # print sess.headers
                file_response = sess.get(file['link'])
                # file_response = sess.get(file['link'], allow_redirects=False)
                file_path = os.path.join(part_dir, file['file_name'])
                print u'保存：', file_path
                # print file_response.history, file_response.text
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)


if __name__ == '__main__':
    get_yearbook_urls()
    get_pages_in_range(year_limit=1)
