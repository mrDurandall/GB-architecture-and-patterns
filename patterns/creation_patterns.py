from copy import deepcopy


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Athlete(User):
    pass


class Coach(User):
    pass


class UserFactory:
    types = {
        'athlete': Athlete,
        'coach': Coach,
    }

    @classmethod
    def create(cls, type_, name, age):
        return cls.types[type_](name, age)


class TrainingPrototype:

    def clone(self):
        return deepcopy(self)


class Training(TrainingPrototype):

    def __init__(self, time, coach, category):
        self.time = time
        self.coach = coach
        self.category = category
        self.category.trainings.append(self)


class AdultTraining(Training):

    def __init__(self, time, coach, category):
        Training.__init__(self, time, coach, category)
        self.type_ = 'Adult'


class ChildrenTraining(Training):

    def __init__(self, time, coach, category):
        Training.__init__(self, time, coach, category)
        self.type_ = 'Children'


class TrainingFactory:
    types = {
        'adult': AdultTraining,
        'children': ChildrenTraining,
    }

    @classmethod
    def create(cls, type_, time, coach, category):
        return cls.types[type_](time, coach, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.trainings = []

    def training_count(self):
        return len(self.trainings)


class Engine:

    def __init__(self):

        self.coaches = []
        self.athletes = []
        self.trainings = []
        self.categories = []

        # Заполним данные для тестирования
        self.coaches.append(UserFactory.create('coach', 'Popov Dmitriy', '34'))
        self.coaches.append(UserFactory.create('coach', 'Volkova Lubov', '30'))
        self.athletes.append(UserFactory.create('coach', 'Adam Ondra', '28'))
        self.athletes.append(UserFactory.create('coach', 'Stasha Gejo', '24'))
        new_category = Category('Morning', None)
        self.categories.append(new_category)
        new_category = Category('Evening', None)
        self.categories.append(new_category)

    @staticmethod
    def create_user(type_, name, age):
        return UserFactory.create(type_, name, age)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Категория с id {id} отсутствует в базе!')

    @staticmethod
    def create_training(type_, time, coach, category):
        return TrainingFactory.create(type_, time, coach, category)

    def get_training_by_coach(self, coach):
        results = []
        for training in self.trainings:
            if training.coach == coach:
                results.append(training)
        return results

