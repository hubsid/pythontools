import json

import common.util
from pythontools.categories import const, util
from pythontools.iam.api.userapi import UserApi
from pythontools import common

api = UserApi(pc_ip=common.util.get_pc_ip_from_env())

# r = api.create('someuser', '03d0e8e1-c53b-5900-a4cd-7b6114a2e63a')
# r = api.get('955d732a-2b9b-54c8-ac14-f6ded42dfe38')
r = api.list()
print(r.status_code)

print(r.json())