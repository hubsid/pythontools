from pythontools.common import const

RDM_DEPLOY_URL='https://rdm.eng.nutanix.com/api/v1/scheduled_deployments'
RDM_DEFAULT_SETTINGS_URL='https://rdm.eng.nutanix.com/api/v1/settings?raw_query={"name":"rdm_defaults"}'
RDM_SMOKE_PASSED_URL='https://rdm.eng.nutanix.com/artifacts?tags=SMOKE_PASSED&product=pc&branch=master'
DEPLOYMENT_REQUEST_BODY={
	'root': {"client_timezone_offset":-330,"comment":"","duration":24,"max_wait_time_till_allocation":48,"name":"","resource_specs":[],"retry":0,"tags":["sidharth_r"]},
	'pe': {"auto_generate_cluster_name":True,"datacenter":{"use_host_names":True},"dod_config":{"allow_nutanix_for_sudo_exec":False,"enable":False,"enable_sudo_restriction":False},"enable_lacp":False,"enable_large_partitions":False,"enable_network_segmentation":False,"hardware":{"all_flash_cluster":False,"cluster_min_nodes":1,"min_host_gb_ram":16,"svm_gb_ram":16,"svm_num_vcpus":8},"image_resource":True,"is_nested_base_cluster":False,"is_new":True,"name":"lucky-moon-14544935","network":{"dc_local":True,"subnet_local":True},"rdma_passthrough":False,"register_prism_to_vcenter":False,"set_cluster_external_ip_address":False,"set_external_data_services_ip_address":False,"software":{"hypervisor":{"type":"ahv","version":"branch_symlink"},"nos":{"build_type":"release","redundancy_factor":"default","version":"master"}},"type":"$NOS_CLUSTER","use_fast_foundation":False,"use_foundation_vm":False},
	'pc': {"dependencies":[],"is_new":True,"name":"autumn-smoke-36825866","prism_elements":[{"host":""}],"provider":{"host":""},"scaleout":{},"software":{"prism_central":{"build_url":"","pc_build_url":"","version":"master"}},"type":"$PRISM_CENTRAL"},
	'nodepool': {
		'global': {"infra":{"kind":"PRIVATE_CLOUD","params":{"category":"general"}},"type":"node_pool"},
		'private': {"entries":["prism-real-node"],"infra":{"kind":"ON_PREM"},"type":"node_pool"}
	},
	'scaleout': {
		'withcmsp': {"cmsp_network":{"type":"vxlan"},"enable_anc":False,"enable_cmsp":True,"iam":"v2","num_instances":1,"pc_domain_name":"cmspdomain.nutanix.com","pcvm_size":"small"},
		'withoutcmsp': {"enable_cmsp":False,"num_instances":1,"pcvm_size":"small"}
	}
}

import os
import random
import requests


def main(name, nodepool, nocmsp, duration):
	# print(f'nocmsp:{nocmsp}, duration:{duration}')
	print('\nBUILDING REQUEST\n...')
	req_body = DEPLOYMENT_REQUEST_BODY['root']
	req_body['name'] = name or (os.environ.get('USER', '') + '-' + str(random.random()))
	req_body['duration'] = duration

	pe = DEPLOYMENT_REQUEST_BODY['pe']
	pe['resources'] = DEPLOYMENT_REQUEST_BODY['nodepool'][nodepool]
	pe_name = req_body['name'] + '-pe'
	pe['name'] = pe_name

	pc = DEPLOYMENT_REQUEST_BODY['pc']
	pc['name'] = req_body['name'] + '-pc'
	pc['dependencies'].append(pe_name)
	pc['prism_elements'][0]['host'] = pe_name
	pc['provider']['host'] = pe_name
	pc['scaleout'] = DEPLOYMENT_REQUEST_BODY['scaleout']['withoutcmsp'] if nocmsp else DEPLOYMENT_REQUEST_BODY['scaleout']['withcmsp']
	pc['software']['prism_central']['pc_build_url'] = get_pc_build_url()
	pc['software']['prism_central']['build_url'] = get_build_url()

	req_body['resource_specs'].append(pe)
	req_body['resource_specs'].append(pc)

	print('SENDING DEPLOYMENT REQUEST\n\n')

	res = requests.post(url=RDM_DEPLOY_URL, json=req_body, auth=const.RDM_AUTH, verify=False)
	return res
	# os.system(f'echo \'{json.dumps(req_body)}\' | subl')

def get_pc_build_url():
	res = requests.get(RDM_DEFAULT_SETTINGS_URL, verify=False).json()
	try:
		return res['data'][0]['data']['prism_central']['pc_build_url']
	except KeyError as e:
		raise Exception('key error while getting pc_build_url:{e}')


def get_build_url():
	res = requests.get(RDM_SMOKE_PASSED_URL, verify=False).json()
	try:
		files = res['result']['data'][0]['files']
		for file in files:
			if file['file_type'] == 'pc-1-click-deploy':
				return os.path.dirname(file['download_url']) + '/'
		raise Exception('problem getting build_url, no file_types \'pc-1-click-deploy\' exist')
	except KeyError:
		raise Exception('key error while getting build_url:{e}')
