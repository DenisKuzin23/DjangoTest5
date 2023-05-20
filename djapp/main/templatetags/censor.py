from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, arg):
    return value.replace(arg, ''.join(['*' for c in arg]))
