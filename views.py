from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html')
