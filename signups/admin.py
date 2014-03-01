from django.contrib import admin
from signups.models import Person

class PersonAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('name', 'email', 'is_added')
	list_filter = ('is_added',)

admin.site.register(Person, PersonAdmin)
