from django import template

register = template.Library()


@register.filter(name="to_class_name")
def to_class_name(value):
    return value.__class__.__name__


@register.filter(name="list_to_name")
def list_to_name(value):
    if value:
        return value[0].__class__.__name__
    else:
        return "None of those labs logged!"


@register.filter(name="get_lab")
def get_lab(dictionary, value):
    return dictionary.get(value)
