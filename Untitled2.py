import os
import json
import csv
import copy
from datetime import datetime
with open('output_1.json','r') as f:
   list = json.load(f)
with open('output_2.json','r') as f:
    list += json.load(f)

with open('output_3.json','r') as f:
    list += json.load(f)
    
with open('output_4.json','r') as f:
    list += json.load(f)

user = {}
ulst = []
for l in list:
    if not 'userPoint' in l:
        continue
    else: 
        user['id'] = l['userPoint']['userId']
        user['createTime'] = l['createTime']
        user['gender'] = l['profile']['gender']
        user['nickname'] = l['profile']['nickname']
        user['province'] = l['profile']['province']
        user['city'] = l['profile']['city']
        user['createDays'] = l['createDays']
    flg = True
    for u in ulst:
        if u['createTime'] == user['createTime']:
            flg = False
    if flg:
        ulst.append(copy.deepcopy(user))


with open('output.csv', 'w', newline='', encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(['id','createTime','createDays','gender','nickname','province','city'])
    for u in ulst:
        w.writerow([u['id'],datetime.fromtimestamp(u['createTime']/1000.0),u['createDays'],u['gender'],u['nickname'],u['province'],u['city']])
