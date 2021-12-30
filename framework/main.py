from quopri import decodestring

from framework.requests import GetRequest, PostRequest


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

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_parameters(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Received post-request {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequest().get_request_parameters(environ)
            request['request_parameters'] = Framework.decode_value(request_params)
            print(f'Received get-request {Framework.decode_value(request_params)}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()
        response, template = view(request)
        start_response(response, [('Content-Type', 'text/html')])
        return [template.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
