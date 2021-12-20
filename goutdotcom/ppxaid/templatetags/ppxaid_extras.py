from django import template

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter(name='get_key')
def get_key(dictionary, key):
    return dictionary.get(key)
