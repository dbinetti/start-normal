# Django
from django import template

register = template.Library()

@register.filter
def location(value):
    if value == 'Unincorporated San Mateo County':
        return 'Unincorporated Area'
    elif value == 'Outside of San Mateo County':
        return 'Outside County'
    else:
        return value
