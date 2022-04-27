from random import random

AAA_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

def create_category_name():
    return 'cat_' + str(random())

def create_category_description():
    return 'cat_desc_' + str(random())
