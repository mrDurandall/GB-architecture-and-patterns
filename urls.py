from views import Index, ContactUs, AboutUs, Trainings, Coaches, Athletes, TrainingCategories

routes = {
    '/': Index(),
    '/contact_us/': ContactUs(),
    '/about_us/': AboutUs(),
    '/trainings/': Trainings(),
    '/training_categories/': TrainingCategories(),
    '/coaches/': Coaches(),
    '/athletes/': Athletes(),
}
