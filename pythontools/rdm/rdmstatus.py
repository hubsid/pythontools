from pythontools.common import const

SCHEDULED_DEPLS_URL='https://rdm.eng.nutanix.com/api/v1/filter/scheduled_deployments?start=0&limit={lastn}&sort=-created_at&raw_query={query}'
GET_DEPL_URL='https://rdm.eng.nutanix.com/api/v1/deployments/{id}'
FILTER_QUERY='''{{
    "$and": [
        {{
            "client.owner": {{
                "$in": [
                    "{user}"
                ]
            }}
        }}
        {active}
    ]
}}'''
ACTIVE_FILTER='''
,
        {
            "status": {
                "$in": [
                    "SUCCESS",
                    "PROCESSING",
                    "PENDING",
                    "PRE_PENDING",
                    "REQUESTING_RESOURCES",
                    "RESOURCES_ALLOCATED"
                ]
            }
        }
'''
TMP_FILE='/tmp/rdmstatusresulttmp'
FIELDS_MAP_PRIMARY={
	# 'id': lambda m: m['_id']['$oid'],
	# 'name': lambda m: m['name'],
	'msg': lambda m: m['message'],
	'progress': lambda m: m['percentage_complete'],
	'rdm_link': lambda m: m['log_view'],
	'with_cmsp': lambda m: getcmsp(m),
	'expires_in': lambda m: format_expiry(m['expires_at']['$date'])
}
FIELDS_MAP_SECONDARY={
	# 'id': lambda m: m['_id']['$oid'],
	# 'name': lambda m: m['name'],
	'type': lambda m: m['type'],
	'msg': lambda m: m['message'],
	'progress': lambda m: m['percentage_complete'],
	'resources': lambda m: m['resources']['type'] + '/' + m['resources']['entries'][0],
	'ip': lambda m: m['allocated_resource'].get('svm_ip', None) or m['allocated_resource'].get('ip', None),
	'log_link': lambda m: m['log_link'],
	'resource_name': lambda m: m['allocated_resource']['name']
}
PRIMARY_FIELDS_SHOW_ALWAYS=['rdm_link', 'with_cmsp', 'expires_in']
PRIMARY_FIELDS_SHOW_ON_FAILURE=['msg', 'progress']
SECONDARY_FIELDS_SHOW_ALWAYS=['type', 'resources']
SECONDARY_FIELDS_SHOW_ON_SUCCESS=['ip', 'resource_name']
SECONDARY_FIELDS_SHOW_ON_FAILURE=['msg', 'progress', 'log_link']

import threading
import time
import requests


def main(lastn=1, active=False, user=const.RDM_USERNAME):
	if lastn is None:
		lastn = 1
	if active is None:
		active = False
	if user is None:
		user = const.RDM_USERNAME

	url = SCHEDULED_DEPLS_URL.format(lastn=lastn, query=make_query(active, user))

	print(f'getting status of last {lastn} {"active" if active else ""} deployment(s) by {user}\n from url:{url}\n\n')

	res = requests.get(url, verify=False)

	if res.status_code != 200:
		print(f'\n\nFAILURE\nstatus_code:{res.status_code}\nRESPONSE---\n{res.text}')
		return

	depl_list = res.json()['data']
	depl_display_list = []
	sec_depl_callables = []

	for depl in depl_list:
		depl_display = {}

		for field in PRIMARY_FIELDS_SHOW_ALWAYS:
			try:
				depl_display[field] = FIELDS_MAP_PRIMARY[field](depl)
			except KeyError:
				# print('thee is a key error while fetching field:{field}')
				pass

		status = depl['status']
		depl_display['status'] = status

		if status == 'FAILED':
			for field in PRIMARY_FIELDS_SHOW_ON_FAILURE:
				depl_display[field] = FIELDS_MAP_PRIMARY[field](depl)
		
		def sec_depl_func(original_depl=depl, display_depl=depl_display):
			sec_depl_list = get_secondary_deployments(original_depl)
			display_depl['secondary_deployments'] = sec_depl_list

		sec_depl_callables.append(sec_depl_func)

		depl_display_list.append(depl_display)

	run_parallel(sec_depl_callables)

	return depl_display_list

def run_parallel(callables):
	threads = []
	for callable in callables:
		t = threading.Thread(target=callable)
		threads.append(t)
		t.start()

	for t in threads:
		t.join()

def make_query(active, user):
	return FILTER_QUERY.format(
		user=user,
		active=(ACTIVE_FILTER if active else '')).replace('\n', '').replace(' ', '')

def get_secondary_deployments(depl):
	id_objs = depl['deployments']

	if not id_objs:
		return None

	sec_depl_list = []
	sec_depl_callables = []

	for id_obj in id_objs:
		id = id_obj['$oid']
		sec_depl_display = {}

		def fill_sec_depls(sec_depl_id=id, sec_depl_fill_in=sec_depl_display):
			sec_depl = requests.get(GET_DEPL_URL.format(id=sec_depl_id), verify=False).json()['data']

			status = sec_depl['status']
			sec_depl_fill_in['status'] = status

			
			for field in SECONDARY_FIELDS_SHOW_ALWAYS:
				try:
					sec_depl_fill_in[field] = FIELDS_MAP_SECONDARY[field](sec_depl)
				except KeyError:
					# sec_depl_fill_in[field] = 'key absent'
					pass

			if status == 'SUCCESS':
				for field in SECONDARY_FIELDS_SHOW_ON_SUCCESS:
					try:
						sec_depl_fill_in[field] = FIELDS_MAP_SECONDARY[field](sec_depl)
					except KeyError:
						# sec_depl_fill_in[field] = 'key absent'
						pass
			else:
				for field in SECONDARY_FIELDS_SHOW_ON_FAILURE:
					try:
						sec_depl_fill_in[field] = FIELDS_MAP_SECONDARY[field](sec_depl)
					except KeyError:
						# sec_depl_fill_in[field] = 'key absent'
						pass

		sec_depl_callables.append(fill_sec_depls)
		sec_depl_list.append(sec_depl_display)

	run_parallel(sec_depl_callables)
	return sec_depl_list

def getcmsp(data):
	try:
		for res_spec in data['payload']['resource_specs']:
			if res_spec['type'] == '$PRISM_CENTRAL':
				return res_spec['scaleout']['enable_cmsp']
	except KeyError:
		return False

def format_expiry(time_secs):
	# print(f'type of time_secs: {type(time_secs)}')

	rem_time = int(time_secs/1000 - time.time())

	days = rem_time//86400
	hours = rem_time//3600 - days*24
	minutes =  rem_time//60 - hours*60 - days*24*60

	# return [days, hours, minutes]

	day_str = '' if days == 0 else f'{days} day' if days == 1 else f'{days} days'
	hour_str = '' if (days > 4 or hours == 0) else f'{hours} hour' if hours == 1 else f'{hours} hours' 
	minute_str = '' if (hours > 4 or minutes == 0) else f'{minutes} minute' if minutes == 1 else f'{minutes} minutes'

	return (day_str + ' ' + hour_str + ' ' + minute_str).lstrip().rstrip()
