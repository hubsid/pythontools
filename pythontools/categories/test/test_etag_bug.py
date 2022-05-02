import logging

from pythontools.categories import util, v4api
from pythontools.common.combinator import Combinator

logging.basicConfig(filename='~/Documents/office/etag bug.log', encoding='utf-8', level=logging.INFO)

class Actions:
    cc = 'create category'
    cc_name_only = 'name only'
    cc_name_and_usname = 'name and usname'
    dsc1 = 'description1'
    usname1 = 'usname1'
    dsc2 = 'description2'
    usname2 = 'usname2'
    keep = 'keep'
    remove = 'remove'
    update = 'update'

combinator_data = {
    Actions.cc: [Actions.cc_name_only, Actions.cc_name_and_usname],
    Actions.dsc1: [Actions.keep, Actions.update, Actions.remove],
    Actions.usname1: [Actions.keep, Actions.update, Actions.remove],
    Actions.dsc2: [Actions.keep, Actions.update, Actions.remove],
    Actions.usname2: [Actions.keep, Actions.update, Actions.remove]
}

api = v4api.V4CategoriesApi(pc_ip=util.get_pc_ip_from_env())

def test(combinator_input):
    funame = 'userSpecifiedName'
    fdesc = 'description'

    if combinator_input[Actions.cc] == Actions.cc_name_only:
        res = api.create({'name': util.create_category_name(), })
    else:
        res = api.create({'name': util.create_category_name(), 'description': util.create_category_description()})

    ext_id = res.json()['data']['extId']

    res = api.getone(ext_id)
    cat = res.json()['data']
    etag = res.headers['Etag']

    if combinator_input[Actions.dsc1] == Actions.update:
        cat[fdesc] = util.create_category_description()
    elif combinator_input[Actions.dsc1] == Actions.remove:
        if cat.get(fdesc, None):
            cat.pop(fdesc)

    if combinator_input[Actions.usname1] == Actions.update:
        cat[funame] = util.create_category_userspecifiedname()

    elif combinator_input[Actions.usname1] == Actions.remove:
        if cat.get(funame, None):
            cat.pop(funame)

    api.update(ext_id, etag, cat)

    # ROUND 2----
    res = api.getone(ext_id)
    cat = res.json()['data']
    etag = res.headers['Etag']

    if combinator_input[Actions.dsc2] == Actions.update:
        cat[fdesc] = util.create_category_description()
    elif combinator_input[Actions.dsc2] == Actions.remove:
        if cat.get(fdesc, None):
            cat.pop(fdesc)

    if combinator_input[Actions.usname2] == Actions.update:
        cat[funame] = util.create_category_userspecifiedname()

    elif combinator_input[Actions.usname2] == Actions.remove:
        if cat.get(funame, None):
            cat.pop(funame)

    res = api.update(ext_id, etag, cat)

    if res.status_code != 200:
        print(res.text)

    assert res.status_code == 200

def run():
    combinator = Combinator(combinator_data)
    combinator.create_combinations()
    # print(combinator.output)
    # exit()
    for combination in combinator.output:
        name = combination['name']
        values = combination['values']

        logging.info('='*50 + name)

        try:
            test(values)
            logging.info('success')
        except Exception as e:
            logging.exception(e)
            # traceback.print_exc()

if __name__ == '__main__':
    run()