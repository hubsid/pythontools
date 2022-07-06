from pythontools.common.util import get_pc_ip_from_env
from  pythontools.iam import  createrole

if __name__ == '__main__':
    for i in range(10):
        createrole.create_role(get_pc_ip_from_env(), 'samplerole-' + str(i))