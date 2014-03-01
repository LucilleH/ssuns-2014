from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.core.validators import email_re

from signups.models import Person
from signups.forms import PersonForm

def submit(request):
	if request.method == 'POST':
		form = PersonForm(request.POST)
		# print formset.errors
		if form.is_valid():
			# Simple spam-prevention technique
			if not request.POST.get('email', '').startswith('http://'):
				person = form.save()
				person.save()
		
			title = 'Successful signup'
			message = 'Thank you for signing up for our listserv.'

			data = {
				'title': title,
				'message': message
			}

			return render(request, 'confirmation.html', data)

	else:
		form = PersonForm()

	data = {
		'form': form,
		'page': {
			'long_name': 'signup listserv',
		},
	}

	return render(request, "listserv.html", data)

