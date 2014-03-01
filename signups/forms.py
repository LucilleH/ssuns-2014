import re

from signups.models import Person

from django import forms


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = (
			'name',
			'email',
			'is_added',
		)
