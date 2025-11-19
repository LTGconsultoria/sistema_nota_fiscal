# seu_app/templatetags/ftp_extras.py
from django import template

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def rfind(value, arg):
    idx = value.rfind(arg)
    if idx == -1:
        return value
    return value[:idx]