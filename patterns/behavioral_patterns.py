from abc import ABCMeta, abstractmethod

from framework.templator import render


# Создание наблюдателя для изменения тренировки
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


# Создание шаблонов для отображений
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list_template.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
