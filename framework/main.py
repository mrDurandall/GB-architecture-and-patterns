class PageNotFound:
    def __call__(self, *args, **kwargs):
        return '404 Not found', 'Oops! 404'


class Framework:

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()
        response, template = view(request)
        start_response(response, [('Content-Type', 'text/html')])
        return [template.encode('utf-8')]