import os

import requests

from pythontools.common import const
from pythontools.rdm import rdmstatus

RDM_EDIT_URL= 'https://rdm.eng.nutanix.com/api/v1/scheduled_deployments'

def extend_expiry(deployment_id, duration):
	url = RDM_EDIT_URL + '/' + deployment_id
	print(f'making request to {url} with auth:{const.RDM_AUTH}')
	return requests.put(url=url, json={'duration': duration}, auth=const.RDM_AUTH, verify=False)

def main(duration, deployment_id, nthlast=0):
	id = None
	if deployment_id:
		id = deployment_id
	else:
		depls = rdmstatus.main(lastn=3, active=True)
		if not depls:
			return False, 'there are no active deployments currently.'
		else:
			depl = None

			if len(depls) > 1:
				print(f'MORE THAN ONE ACTIVE DEPLOYMENTS, TRYING TO EXTEND {nthlast} th DEPLOYMENT:\n{depls}')
				try:
					depl = depls[nthlast]
				except ValueError:
					return False, f'there are only {len(depls)} deployments, please enter a proper range for nthlast param from 0 to {len(depls) - 1}'
			else:
				depl = depls[0]

			id = os.path.split(depl['rdm_link'])[1]

	print(f'extending expiry of deployment with id:{id} by {duration} hours')
	res = extend_expiry(id, duration)
	return True, res
