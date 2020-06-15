from random import randint
from simhash import hashlib


class Random_Check_generate:#随机字符串生成
    def __init__(self):
        self.generate_int_seed=randint(2020,99999999999999999)
        self.rand_flag=hashlib.md5(str(self.generate_int_seed).encode('utf-8'))
    def Get_randstring(self):
        return self.rand_flag.hexdigest()

