# from os.path import join

from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class ContactUs:
    def __call__(self, request):
        if request['method'] == 'POST':
            with open('messages.txt', 'a') as f:
                for data in list(request['data'].values())[:3]:
                    f.write(f'{data}\n')
                f.write('\n')
        return '200 OK', render('contact.html')


class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html')
