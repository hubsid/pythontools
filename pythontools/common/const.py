import os
import subprocess
from enum import Enum

import requests

V3_GROUPS_URL='https://{host}:9440/api/nutanix/v3/groups'
QA_DOMAIN='qa.nutanix.com'

APPLICATION_JSON_HEADER = {'Content-Type': 'application/json'}

PC = os.environ.get('PC')
UBVM = os.environ.get('UBVM')
PC_PASS = 'nutanix/4u'
OKTA_PASS = subprocess.run(['sh', '-c', 'oktapswd.sh | base64 -d'], capture_output=True).stdout.decode('utf-8')[0:-1]
RDM_USERNAME='sidharth.r'
RDM_AUTH=requests.auth.HTTPBasicAuth(RDM_USERNAME, OKTA_PASS)
ADMIN_AUTH = requests.auth.HTTPBasicAuth('admin', 'Nutanix.123')


class Identifier(Enum):
	UUID = 1
	NAME = 2


class Operation(Enum):
	ADD = 1
	REMOVE = 2
	SET = 3
	CLEAR = 4