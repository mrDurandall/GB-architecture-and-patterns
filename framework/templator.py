from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):

    current_environment = Environment()
    current_environment.loader = FileSystemLoader(folder)
    template = current_environment.get_template(name=template_name)

    return template.render(**kwargs)
