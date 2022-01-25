from copy import deepcopy
from sqlite3 import connect

from patterns.behavioral_patterns import TrainingObserver, EmailNotifier, SMSNotifier, FileWriter,\
    ConsoleWriter
from patterns.unit_of_work import DomainObject


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


class Training(TrainingPrototype, TrainingObserver):

    next_id = 1

    def __init__(self, time, coach, category):
        self.id = Training.next_id
        Training.next_id += 1
        self._time = time
        self._coach = coach
        self.category = category
        self.category.trainings.append(self)
        self.athletes = []
        super().__init__()

    def __getitem__(self, item):
        return self.athletes[item]

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, new_time):
        self._time = new_time
        self.notify_time()

    @property
    def coach(self):
        return self._coach

    @coach.setter
    def coach(self, new_coach):
        self._coach = new_coach
        self.notify_coach()

    def add_athlete(self, athlete):
        self.athletes.append(athlete)


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

    def get_training_by_id(self, id):
        for training in self.trainings:
            if training.id == id:
                result = training
                return result
        raise Exception(f'There is no training with {id} id in base!')

    def get_athlete_by_name(self, name):
        for athlete in self.athletes:
            if athlete.name == name:
                return athlete
        raise Exception(f'There is no athlete with {name} name in base!')



class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log-->{text}'
        self.writer.write(text)


class AthleteMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'athletes'

    def all(self):
        statment = f'SELECT * FROM {self.tablename}'
        self.corsor.execute(statment)
        result = []
        for item in self.cursor.fetchall():
            id, name, age = item
            athlete = Athlete(name, age)
            athlete.id = id
            result.append(athlete)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name, age FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id, ))
        result = self.cursor.fetchone()
        if result:
            return Athlete(*result)
        else:
            raise RecordNotFoundException(f'There is no athlete with id={id}')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name, obj.age, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('elbrus_gym.sqlite')


class MapperRegistry:
    mappers = {
        'athletes': AthleteMapper,

    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Athlete):
            return AthleteMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


if __name__ == '__main__':
    category = Category('Morning', None)
    training = Training('12.00', 'Lubov Volkova', category)
    training.observers.append(EmailNotifier())
    training.observers.append(SMSNotifier())
    training.time = '11.00'
    training.coach = 'Popov Dmitriy'
