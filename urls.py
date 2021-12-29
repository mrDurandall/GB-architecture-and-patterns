from views import Index, ContactUs, AboutUs

routes = {
    '/': Index(),
    '/contact_us/': ContactUs(),
    '/about_us/': AboutUs(),
}
