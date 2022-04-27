import os
from random import random

AAA_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

def create_category_name():
    return 'cat_' + str(random())

def create_category_description():
    return 'cat_desc_' + str(random())

def get_pc_ip_from_env():
    try:
        return os.environ['PC']
    except KeyError:
        print('please provide the PC IP in the environment variable \'PC\'')
        exit(1)
