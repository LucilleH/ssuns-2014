from django.shortcuts import render
from cms.models import Page

def main(request, name='home'):
	try:
		data = {
			'page': Page.objects.get(short_name=name)
		}

		return render(request, 'page.html', data)
	except Page.DoesNotExist:
		return render(request, '404.html')
