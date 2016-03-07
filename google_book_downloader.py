import requests
import json
import re
import sys
import bs4
import os

# url = 'https://books.google.com/books?id=_u18BHJZi9kC&lpg=PP1&pg=PA258#v=onepage&q&f=false' 
url = 'https://books.google.com/books?id=jCXw02NaYvEC&printsec=frontcover&dq=javascript&hl=en&sa=X&ved=0ahUKEwjA4IqBl67LAhUI5WMKHVelCogQuwUIWjAI#v=onepage&q&f=false'
headers = {'cookie': 'OGPC=5061821-2:5061451-1:5061574-1:5061869-1:5061952-2:5061975-7:5061976-1:; OGP=-5061821:-5061451:-5061574:; SID=DQAAAAABAABta7kCQTey5qP6TWgqVo0LoEmOKu7Ar82CpM9HRKx-8O4VQFaS5qe3t_9Qx2W7ewHCMvbEIUHMT2Hfnn6mFevGbUnZGsiJ9CAstBMM9K7_ULS3ZGW4WSV4n8GGRwDqsCxXY9yf3WMj_QQrFgnvA-NJs0sRrArN31JOl1qwEgBCUetT-EtyaBKBfvwXM_mvLfYBDzMuvKwy_sIr0TIi9ELkfpCGptOiqH8rZGsumTDLVxu097nB8g2OgrbpR9I0LcRx_PVZACyPUWd6Um7R3cuXZvPF1DVuI49G5IhgH_3kuwg_Hfx2jdn1g_14nMrsrN9kq74eRHq0XUy6KnkUpXnP; HSID=ASSjKnWKOs9CZ6SYB; SSID=Aum4COF2ZhxqXohR0; APISID=NINWEjbkgJrLYCpL/AMLjRHdr6FZFOAVGI; SAPISID=9M-6Omy9h_NY3Eb7/AJu5dW_mH78tWduu9; NID=77=cHlR858Gx5x7meYtneWjZN92UrJzfALKo_ZysYp3zGUYjpQ6-l_OS0QWL7vk7c5fXhPUuCjYsTyyDdW8cN7If6WwEtZIsqPoSDU5uHD2AbJbnn4fmHcVqM94TGYKAvlI1oSXDhIoXLKWTFPetgXbwfJ7PF48BLGE1aWqTIV5a7s-H8x5__w-ENaYGX6v6HSIo9Z3IKx79kfEEYzwBTKafBmkPcJ8nAR5m_D_3puOsDY4DREfG0ANNYJmlupEgVDQPYba9_mgnMPMNm6fMBFgoyf-6Q; __utma=20549163.1228662765.1456845141.1457326166.1457328849.8; __utmz=20549163.1457328849.8.7.utmcsr=askubuntu.com|utmccn=(referral)|utmcmd=referral|utmcct=/questions/510340/google-books-downloader-for-ubuntu; __utmc=20549163; __utmb=20549163.14.10.1457328849; __utmt=1'}

r = requests.get(url, headers=headers)
html = bs4.BeautifulSoup(r.text)
book_title = html.title.string
print book_title


base_url = url.split('#')[0]
PAGE_API_POSTFIX = '&jscmd=click3'
page_api = base_url + PAGE_API_POSTFIX

# info_api = 'https://books.google.com/books?id=_u18BHJZi9kC&lpg=PP1&pg=PR8' + '&jscmd=click3'

results = {}

r = requests.get(page_api, headers=headers)
print page_api
pages = r.json()['page']
for page in pages:
    pid = page['pid']
    src = page.get('src')
    if src:
        print(pid, src)
    if results.get(pid) is None:
        results[pid] = src

print ('total page: %d' % len(results.keys()) )
print results

# strip off the '&pg=xxx'
base_url = re.sub('&pg.*', '', base_url)

for pid in results.keys()[:3]:
    if results[pid] is None:
        page_api = base_url + '&pg=' + pid + PAGE_API_POSTFIX
        # debug
        print page_api
        r = requests.get(page_api, headers=headers)
        pages= r.json()['page']
        for page in pages:
            src = page.get('src')
            if src:
                pid = page['pid']
                if results.get(pid) is None:
                    results[pid] = src
                    # debug
                    print(pid, src)
print results
with open('data.txt', 'w') as outfile:
    json.dump(results, outfile, sort_keys=True)


if not os.path.exists(book_title):
    os.makedirs(book_title)

os.chdir(book_title)
for pid, url in results.iteritems():
    if url:
        filename = '%s.png' % pid
        response = requests.get(url, headers=headers)
        with open(filename, 'wb') as f:
            f.write(response.content)
            print '%s saved.' % filename
print 'All pages saved.'
