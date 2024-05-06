import hashlib, random

from datetime import datetime

def format_date(now, format = '%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(now, format)

def gen_random_code():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'
    seed = ''.join(random.sample(alphabet, 10))
    h_md5 = hashlib.md5()
    h_md5.update(seed.encode('utf-8'))
    return h_md5.hexdigest()