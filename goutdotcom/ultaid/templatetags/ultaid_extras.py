from django import template

register = template.Library()

@register.filter(name='get_ultaid')
def get_ultaid(dictionary, key):
    return dictionary.get(key)
