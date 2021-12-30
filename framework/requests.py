class Request:

    @staticmethod
    def split_parameters(parameters_string):
        parameters = {}
        if parameters_string:
            splited_string = parameters_string.split('&')
            for parameter in splited_string:
                key, value = parameter.split('=')
                parameters[key] = value
        return parameters


class GetRequest(Request):

    def get_request_parameters(self, environ):
        query_string = environ['QUERY_STRING']
        parameters = self.split_parameters(query_string)
        return parameters


class PostRequest(Request):

    @staticmethod
    def get_wsgi_input_data(environ):
        content_length = environ.get('CONTENT_LENGTH')
        content_length = int(content_length) if content_length else 0
        print(content_length)
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        print(data)
        return data

    def split_wsgi_parameters(self, data):
        parameters = {}
        if data:
            data_string = data.decode(encoding='utf-8')
            print(f'after decode {data_string}')
            parameters = self.split_parameters(data_string)
        return parameters

    def get_request_parameters(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.split_wsgi_parameters(data)
        return data

