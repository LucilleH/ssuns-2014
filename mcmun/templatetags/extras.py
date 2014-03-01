from django import template

register = template.Library()

@register.filter
def get_range(end, start=1):
	"""
	Filter - returns a list containing range made from given value

	"""
	return range(start, end + 1)
