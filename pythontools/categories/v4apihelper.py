from pythontools.categories import util
from pythontools.categories.v4api import V4CategoriesApi

class V4CategoriesApiHelper(V4CategoriesApi):
    def create_with_name(self):
        return self.create({'name': util.create_category_name()})

    def create_with_name_desc(self):
        return self.create({'name': util.create_category_name(),
                           'description': util.create_category_description()})

    def update_with_etag(self, ext_id, remove, include):
        res = self.getone(ext_id)
        assert res.status_code == 200
        etag = res.headers['Etag']
        cat = res.json()['data']

        for item in remove:
            if cat.get(item, None):
                cat.pop(item)
        cat.update(include)
        print(f'updating with body:{cat}')

        return self.update(ext_id, etag, cat)


