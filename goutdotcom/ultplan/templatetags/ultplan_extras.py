from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter(name="get_key")
def get_key(dictionary, key):
    return dictionary.get(key)


@register.filter(name="duration_in_days")
def duration_in_days(duration):
    """
    Format a duration field to return only XXX days
    returns: str
    """
    total_seconds = int(duration.total_seconds())
    total_days = total_seconds // 3600 // 24
    return f"{total_days} days"
