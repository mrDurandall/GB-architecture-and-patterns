from wsgiref.simple_server import make_server

from framework.main import Framework
from urls import routes


if __name__ == '__main__':

    NewApplication = Framework(routes)

    with make_server('', 8000, NewApplication) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
