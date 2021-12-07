from django import template

register = template.Library()

@register.filter(name='get_flare')
def get_flare(dictionary, key):
    return dictionary.get(key)
