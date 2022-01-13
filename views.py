from framework.templator import render

from patterns.creation_patterns import Engine, Logger

site = Engine()


class Index:
    def __call__(self, request):
        Logger.log('Index page opened')
        return '200 OK', render('index.html')


class ContactUs:
    def __call__(self, request):
        Logger.log('Contact page opened')
        if request['method'] == 'POST':
            with open('messages.txt', 'a') as f:
                for data in list(request['data'].values())[:3]:
                    f.write(f'{data}\n')
                f.write('\n')
        return '200 OK', render('contact.html')


class AboutUs:
    def __call__(self, request):
        Logger.log('About page opened')
        return '200 OK', render('about_us.html')


class TrainingCategories:
    def __call__(self, request):
        Logger.log('Categories page opened')
        return '200 OK', render('training_categories.html', objects_list=site.categories)


class Trainings:
    def __call__(self, request):
        Logger.log('Trainings page opened')
        category_id = int(request['request_parameters']['id'])
        category = site.find_category_by_id(category_id)
        if request['method'] == 'POST':
            data = request['data']
            time = data['time']
            coach = data['coach']
            type_ = data['type']
            new_training = site.create_training(type_, time, coach, category)
            site.trainings.append(new_training)
        return '200 OK', render('trainings.html',
                                objects_list=category.trainings,
                                category_name=category.name,
                                coaches_list=site.coaches)


class Coaches:
    def __call__(self, request):
        Logger.log('Coaches page opened')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            age = data['age']
            new_coach = site.create_user('coach', name, age)
            site.coaches.append(new_coach)
        return '200 OK', render('coaches.html', objects_list=site.coaches)


class Athletes:
    def __call__(self, request):
        Logger.log('Athletes page opened')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            age = data['age']
            new_coach = site.create_user('athlete', name, age)
            site.athletes.append(new_coach)
        return '200 OK', render('athletes.html', objects_list=site.athletes)
