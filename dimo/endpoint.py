from request import Request

class Endpoint:

    def __init__(self, name, basic_methods, session):
        self.name = name
        self.session = session
        self._add_basic_methods(basic_methods)

    def _add_basic_methods(self, basic_methods):
        if not basic_methods:
            return

        uri = f'/{self.name}'
        # TODO: check these based on the way dimo endpoints are structured (eg. URIs - need to analyze )
        if 'GET' in basic_methods:
            self.get = Request('GET', uri, self.session)
        if 'POST' in basic_methods:
            self.post = Request('POST', uri, self.session)

        # uri = f'{uri}/:{self.name[:-1]}Id'  # e.g. '/admins' --> '/admins/:adminId'

        if 'PUT' in basic_methods:
            self.update_usr = Request('PUT', uri, self.session)     #self.update_usr as it's CURRENTLY the only endpoint using PUT
        if 'PATCH' in basic_methods:
            self.update = Request('PATCH', uri, self.session)
        if 'DELETE' in basic_methods:
            self.delete = Request('DELETE', uri, self.session)
