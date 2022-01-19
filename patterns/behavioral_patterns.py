from abc import ABCMeta, abstractmethod


class Notifier(metaclass=ABCMeta):

    @abstractmethod
    def update_time(self, subject):
        pass

    @abstractmethod
    def update_coach(self, subject):
        pass


class TrainingObserver:

    def __init__(self):
        self.observers = []

    def notify_time(self):
        for observer in self.observers:
            observer.update_time(self)

    def notify_coach(self):
        for observer in self.observers:
            observer.update_coach(self)


class SMSNotifier(Notifier):

    def update_time(self, subject):
        print(f'SMS-> Training changed. New time of training: {subject.time}.')

    def update_coach(self, subject):
        print(f'SMS-> Training changed. New coach: {subject.coach}.')


class EmailNotifier(Notifier):

    def update_time(self, subject):
        print(f'Email-> Training changed. New time of training: {subject.time}.')

    def update_coach(self, subject):
        print(f'Email-> Training changed. New coach: {subject.coach}.')

