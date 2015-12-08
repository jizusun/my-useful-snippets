# A very primitive version to extract threads in course forum,
# xuetangx.com is based on Open edX
# Author: sunjizu#gmail.com

from requests import session, get
import json
import codecs

login_ajax = 'http://nju.xuetangx.com/login_ajax'
forum_url = 'http://nju.xuetangx.com/courses/NJU/ELEC003/2014_T2/discussion/forum'
thread_postfix = '/7c523cb8e8f047eaaf195cb247e188ac/threads/'

# bypass csrf when log in

# with session() as c:
#     c.get(forum)
#     csrftoken = c.cookies['csrftoken']
# 
#     payload = {
#         'validate': '',
#         'info':'xxxxx@smail.nju.edu.cn' ,
#         'password': 'xxxxx',
#         'csrfmiddlewaretoken': csrftoken
#     }
#     r = c.post(login_ajax, data=payload)

# use cookie  
headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-with': 'XMLHttpRequest',
        'Cookie': "" # copy the cookie from your browser after you logged in
        }

forum_params = {'ajax' : '1', 
        'page': '1',
        'sort_key' : 'date',
        'sort_order' : 'desc'
        }

response = get(forum_url, params=forum_params, headers=headers)
num_pages = response.json()['num_pages']
thread_ids = {}

for i in range(num_pages):
# for i in range(1):
    forum_params['page'] = i+1
    response = get(forum_url, params=forum_params, headers=headers)
    print(response.url)
    for discuss in response.json()['discussion_data']:
        id = discuss['id']
        thread_ids[id] = discuss['title']

# for k,v in thread_ids.items():
    # print(k),
    # print(v)

count = len(thread_ids.items())
count = str(count)
print("Total threads: " + count)

thread_params = {'ajax': '1', 
        'resp_skip': '0', 
        'resp_limit': '25'
        }

thread_results = {}
for id in thread_ids.keys():
    thread_url = forum_url + thread_postfix + id
    response = get(thread_url, params = thread_params, headers= headers)
    print(response.url)
    content = response.json()['content']
    id = content['title'] + " " + content['id']
    thread_results[id] = content

# http://stackoverflow.com/a/18337754/3074866
# print json.dumps(thread_results, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8')

# http://stackoverflow.com/a/31343739/3074866
with codecs.open('data.txt', 'w', 'utf-8') as f:
    f.write(json.dumps(thread_results,ensure_ascii= False, indent=4, sort_keys=True))
