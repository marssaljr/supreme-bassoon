from django import template

register=template.Library()

@register.filter()
def multiply(v, arg):
		return float(v)*arg
