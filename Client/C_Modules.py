#用于客户端中用到的模块
from random import randint
from simhash import hashlib
import json

class Random_Check_generate:#随机字符串生成
    def __init__(self):
        self.generate_int_seed=randint(2020,99999999999999999)
        self.rand_flag=hashlib.md5(str(self.generate_int_seed).encode('utf-8'))
    def Get_randstring(self):
        return self.rand_flag.hexdigest()




conf={}
with open('./Client/config.json','r') as f:
    conf=json.load(f)

conf['Server_List'].append({'host':'255.225.122.102','port':8777})
for i in conf['Server_List']:
    print(i['host']+':'+i['port'])
print(conf)
    
#    for i in range(0,2):
#        print(e['Server_List'][i]['host']+':'+str(e['Server_List'][i]['port']))

#mm=[['125.55.4.222', 8808], ['125.55.4.222', 8808]]
