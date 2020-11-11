# Allows custom filters and tags to be used in my app
from django import template
register = template.Library()

# Divides the value by the argument and returns the result if possible
@register.filter
def divide(value, arg):
    try:
        return value / arg
    except:
        return "N/A"

# Multiplies the value by the argument and returns the result if possible
@register.filter
def multiply(value, arg):
    try:
        return int(value * arg)
    except:
        return "N/A"
