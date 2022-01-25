from framework.templator import render

from patterns.creation_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import SMSNotifier, EmailNotifier, TemplateView, ListView,\
    CreateView, BaseSerializer


site = Engine()
logger = Logger('main')

routes = {}


# @AppRoute(routes_list=routes, url='/')
# class Index:
#     @Debug(name='Index')
#     def __call__(self, request):
#         Logger.log('Index page opened')
#         return '200 OK', render('index.html')

@AppRoute(routes_list=routes, url='/')
class Index(TemplateView):
    template_name = 'index.html'


# @AppRoute(routes_list=routes, url='/contact_us/')
# class ContactUs:
#     @Debug(name='Contact')
#     def __call__(self, request):
#         Logger.log('Contact page opened')
#         if request['method'] == 'POST':
#             with open('messages.txt', 'a') as f:
#                 for data in list(request['data'].values())[:3]:
#                     f.write(f'{data}\n')
#                 f.write('\n')
#         return '200 OK', render('contact.html')

@AppRoute(routes_list=routes, url='/contact_us/')
class ContactUs(CreateView):
    template_name = 'contact.html'

    def create_object(self, data):
        with open('messages.txt', 'a', encoding='utf-8') as f:
            for data in list(data.values())[:3]:
                f.write(f'{data}\n')
            f.write('\n')


# @AppRoute(routes_list=routes, url='/about_us/')
# class AboutUs:
#     @Debug(name='About')
#     def __call__(self, request):
#         Logger.log('About page opened')
#         return '200 OK', render('about_us.html')

@AppRoute(routes_list=routes, url='/about_us/')
class AboutUs(TemplateView):
    template_name = 'about_us.html'


# @AppRoute(routes_list=routes, url='/training_categories/')
# class TrainingCategories:
#     @Debug(name='Categories')
#     def __call__(self, request):
#         Logger.log('Categories page opened')
#         return '200 OK', render('training_categories.html', objects_list=site.categories)

@AppRoute(routes_list=routes, url='/training_categories/')
class TrainingCategories(ListView):
    template_name = 'training_categories.html'
    queryset = site.categories


@AppRoute(routes_list=routes, url='/trainings/')
class Trainings:
    @Debug(name='Trainings')
    def __call__(self, request):
        logger.log('Trainings page opened')
        category_id = int(request['request_parameters']['id'])
        category = site.find_category_by_id(category_id)
        if request['method'] == 'POST':
            data = request['data']
            time = data['time']
            coach = data['coach']
            type_ = data['type']
            new_training = site.create_training(type_, time, coach, category)
            new_training.observers.append(SMSNotifier())
            new_training.observers.append(EmailNotifier())
            site.trainings.append(new_training)
        return '200 OK', render('trainings.html',
                                objects_list=category.trainings,
                                category_name=category.name,
                                coaches_list=site.coaches)


# @AppRoute(routes_list=routes, url='/coaches/')
# class Coaches:
#     @Debug(name='Coaches')
#     def __call__(self, request):
#         Logger.log('Coaches page opened')
#         if request['method'] == 'POST':
#             data = request['data']
#             name = data['name']
#             age = data['age']
#             new_coach = site.create_user('coach', name, age)
#             site.coaches.append(new_coach)
#         return '200 OK', render('coaches.html', objects_list=site.coaches)

@AppRoute(routes_list=routes, url='/coaches/')
class Coaches(CreateView, ListView):
    template_name = 'coaches.html'
    queryset = site.coaches

    def create_object(self, data):
        name = data['name']
        age = data['age']
        new_coach = site.create_user('coach', name, age)
        logger.log('New coach added')
        site.coaches.append(new_coach)


# @AppRoute(routes_list=routes, url='/athletes/')
# class Athletes:
#     @Debug(name='Athletes')
#     def __call__(self, request):
#         Logger.log('Athletes page opened')
#         if request['method'] == 'POST':
#             data = request['data']
#             name = data['name']
#             age = data['age']
#             new_coach = site.create_user('athlete', name, age)
#             site.athletes.append(new_coach)
#         return '200 OK', render('athletes.html', objects_list=site.athletes)

@AppRoute(routes_list=routes, url='/athletes/')
class Athletes(CreateView, ListView):
    template_name = 'athletes.html'
    queryset = site.athletes

    def create_object(self, data):
        name = data['name']
        age = data['age']
        new_athlete = site.create_user('athlete', name, age)
        logger.log('new atlete added')
        site.athletes.append(new_athlete)


@AppRoute(routes_list=routes, url='/change_training/')
class ChangeTraining:
    def __call__(self, request):
        logger.log('Change trainings page opened')
        training_id = int(request['request_parameters']['id'])
        training = site.get_training_by_id(training_id)
        old_time = training.time
        old_coach = training.coach
        if request['method'] == 'POST':
            data = request['data']
            time = data['time']
            if time != old_time:
                training.time = time
            coach = data['coach']
            if coach != old_coach:
                training.coach = coach
            return '200 OK', render('trainings.html',
                                    objects_list=training.category.trainings,
                                    category_name=training.category.name,
                                    coaches_list=site.coaches)
        return '200 OK', render('change_training.html',
                                objects_list=training,
                                coaches_list=site.coaches)


@AppRoute(routes_list=routes, url='/add_athlete/')
class AddAthlete:
    def __call__(self, request):
        logger.log('Add athlete page opened')
        training_id = int(request['request_parameters']['id'])
        training = site.get_training_by_id(training_id)
        all_athletes = set(site.athletes)
        print(all_athletes)
        training_athletes = set(training.athletes)
        print(training_athletes)
        free_athletes = list(all_athletes.difference(training_athletes))
        print(free_athletes)
        if request['method'] == 'POST':
            data = request['data']
            athlete = site.get_athlete_by_name(data['athlete_name'])
            training.athletes.append(athlete)
            return '200 OK', render('trainings.html',
                                    objects_list=training.category.trainings,
                                    category_name=training.category.name,
                                    coaches_list=site.coaches)
        return '200 OK', render('add_athlete.html',
                                objects_list=free_athletes)


@AppRoute(routes_list=routes, url='/training_api/')
class TrainingApi:

    def __call__(self, request):
        id = int(request['request_parameters']['id'])
        return '200 OK', BaseSerializer(site.get_training_by_id(id)).save()
