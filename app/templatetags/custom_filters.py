from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def get_value(dictionary: dict, key):
    return dictionary.get(key)


@register.filter
def extract_column(queryset: QuerySet, field_name: str) -> list:
    return [getattr(obj, field_name) for obj in queryset]
