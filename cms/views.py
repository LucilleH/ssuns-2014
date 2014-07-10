from django.shortcuts import render
from cms.models import Page

def mobile(request, name='mobile'):
	try:
		data = {
			'page': Page.objects.get(short_name=name)
		}

		return render(request, 'page-mobile.html', data)
	except Page.DoesNotExist:
		return render(request, '404.html')



def main(request, name='home'):
	try:
		data = {
			'page': Page.objects.get(short_name=name)
		}

		return render(request, 'page.html', data)
	except Page.DoesNotExist:
		return render(request, '404.html')

def mobilehome(request, name='mobile-home'):
	return render(request, 'home-mobile.html')