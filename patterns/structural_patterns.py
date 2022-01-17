from time import time


class AppRoute:

    def __init__(self, routes_list, url):
        self.routes = routes_list
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):

        def timeit(func):

            def timed(*args, **kwargs):
                start_time = time()
                result = func(*args, **kwargs)
                end_time = time()
                print(f'debug---> running time of {self.name} was {(end_time - start_time):2.2f}')
                return result

            return timed

        return timeit(cls)

