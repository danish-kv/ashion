from django import template

register = template.Library()


@register.filter(name="div")
def div(value, by):
    try:
        return float(value) / float(by)
    except (ValueError, ZeroDivisionError):
        return 0.0
