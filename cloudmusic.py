import requests
import random
import json
import time 
import copy
import csv
from datetime import datetime
class IP:
    IPS = []
    def __init__(self):
        self.updateIP()
        
    def testConnection(self, ip):
        flag = False
        proxies = {
            "http": 'http://' + ip,
            "https": 'http://' + ip
        }
        try:
            requests.get("http://api.ip.sb/ip",proxies=proxies,timeout=5)
        except:
            flag = True
        return flag

    def updateIP(self):
        url = 'https://proxy.horocn.com/api/proxies?order_id=Y3H91638025710524742&num=10&format=text&line_separator=win'
        if len(self.IPS) == 0:
            response = requests.get(url)
            self.IPS = str(response.content.decode("utf-8")).split('\r\n')
    
    def makeRequest(self, url):
        self.updateIP()
        idx = int(random.random() * (len(self.IPS)))
        if self.testConnection(self.IPS[idx]):
            self.IPS.remove(self.IPS[idx])
            self.updateIP()
            idx = int(random.random() * (len(self.IPS)))
        try:
            rsp = requests.get(url + '&proxy=http://' + self.IPS[idx]).content.decode("utf-8")
        except:
            rsp = '{"code": 404}'
        return rsp
        

def isExisted(obj, list):
    if len(list) == 0:
        return False
    flag = False
    for l in list:
        if obj == l:
            flag = True
            break
    return flag

def getUsers():
    list = []
    ids = []
    url = 'http://localhost:3000/user/detail?uid='
    updateIpCounter = 0;
    ipRequest = IP()
    while len(list) < 5000:
        updateIpCounter += 1
        rid = int(73070177 + random.random() * (1300000531 - 73070177))
        while(isExisted(rid, ids)):
            rid = int(73070177 + random.random() * (1300000531 - 73070177))
        ids.append(rid)
        obj = json.loads(ipRequest.makeRequest(url + str(rid)))
        time.sleep(0.1)
        while 'code' in obj and obj['code']=='404':
            print('try: ', str(updateIpCounter), 'suc: ', str(len(list)), 'suc rate: ', str(len(list)/(updateIpCounter+1)), 'ip pool: ',len(ipRequest.IPS)) 
            rid = rid + 1
            if isExisted(rid, ids):
                break
            ids.append(rid)
            obj = json.loads(ipRequest.makeRequest(url + str(rid)))
            updateIpCounter += 1
        if 'createTime' in obj:
            print(obj['createTime'])
            list.append(obj)
        print('try: ', str(updateIpCounter), 'suc: ', str(len(list)), 'suc-rate: ', str(len(list)/(updateIpCounter+1)), 'ip pool: ',len(ipRequest.IPS))
        if len(list) % 10 == 0:
            with open('output.json', 'w') as f:
                json.dump(list, f)
        
def test():
    url = "http://localhost:3000/song/detail?ids=532013576"
    obj = json.loads(requests.get(url).content.decode("utf-8"))
    print(obj['songs'][0]['id'],obj['songs'][0]['publishTime'],obj['songs'][0]['name'])
    print('id' in obj['songs'][0],'publishTime' in obj['songs'][0],'name' in obj['songs'][0])



def getMusic():
    url = "http://localhost:3000/song/detail?ids="
    ipRequest = IP()
    list = []
    while len(list) < 1000:
        randId = int(60000 + random.random() * (1375857584 - 60000))
        obj = json.loads(ipRequest.makeRequest(url + str(randId)))
        if not 'songs' in obj:
            print('\033[91m','REQUEST ERROR',' [', str(datetime.now()),']','\033[0m')
            time.sleep(5)
            continue
        if len(obj['songs']) == 0:
            print('songs null id=',randId, obj, ' [', str(datetime.now()),']')
            continue
        music = {}
        if (not 'name' in obj['songs'][0]) or (not 'id' in obj['songs'][0]) or (not 'publishTime' in obj['songs'][0]):
            print('attr miss ',obj, ' [', str(datetime.now()),']')
            continue
        if obj['songs'][0]['name'] == '' or obj['songs'][0]['id']=='' or obj['songs'][0]['publishTime'] == '':
            print('attr null ', 'name=',obj['songs']['name'],'id=',obj['songs'][0]['id'],'publishTime=',obj['songs'][0]['publishTime'], ' [', str(datetime.now()),']')
            continue
        if obj['songs'][0]['name'] == 'None' or obj['songs'][0]['publishTime'] == 0:
            print('attr error ','name=',obj['songs'][0]['name'],'publishTime=',obj['songs'][0]['publishTime'],' [', str(datetime.now()),']')
            continue
        flag = False
        for l in list:
            if l['id'] == obj['songs'][0]['id']:
                flag = True
                break
        if flag:
            print('existed ',' [', str(datetime.now()),']')
            continue
        music['name'] = obj['songs'][0]['name']
        music['id'] = obj['songs'][0]['id']
        music['publishTime'] = obj['songs'][0]['publishTime']
        if music['publishTime'] > 1512046799000:
            print('\033[91m','2017 ERROR', music,str(datetime.now()),'\033[0m')
            continue
        list.append(copy.deepcopy(music))
        print('\x1b[6;30;42m' ,'succ ',len(list),'/',str(1000),music,' [', str(datetime.now()),']','\x1b[0m')
        if len(list) % 10 == 0:
            with open('backup.json', 'w') as f:
                json.dump(list,f)
        
    with open('output.csv', 'w', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        w.writerow(['id','name','publishTime'])
        for l in list:
            w.writerow([l['id'], l['name'], datetime.fromtimestamp(l['publishTime']/1000.0)])

getMusic()