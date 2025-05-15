# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def abbreviate_number(value):
    try:
        value = int(value)
        if value >= 1_000_000:
            return f'{value / 1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value / 1_000:.1f}K'
        return str(value)
    except (ValueError, TypeError):
        return value
