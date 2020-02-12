from urllib import quote_plus
import datetime
from django import template

register=template.Library()

@register.filter
def nowyear():
    return datetime.date.year