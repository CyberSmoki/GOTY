from django import template

register = template.Library()

@register.filter
def get_value(dictionary: dict, key):
    return dictionary.get(key)
