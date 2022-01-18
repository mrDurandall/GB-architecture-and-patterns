from abc import ABCMeta, abstractmethod


class Notifier(metaclass=ABCMeta):

    @abstractmethod
    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def update(self):
        for observer in self.observers:
            observer.update(self)


class SMSNotifier(Notifier):

    def update(self, subject):
        print(f'SMS-> Training changed. New date and time of training: {subject.date}, {subject.time}.')


class EmailNotifier(Notifier):

    def update(self, subject):
        print(f'Email-> Training changed. New date and time of training: {subject.date}, {subject.time}.')

