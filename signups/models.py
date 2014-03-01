from django.db import models

class Person(models.Model):
	class Meta:
		ordering = ['name']

	email = models.EmailField(max_length=254, unique=True)
	name = models.CharField(max_length=50)
	is_added = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s <%s>' % (self.name, self.email)
