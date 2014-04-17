from django.contrib import admin
from cms.models import ParentPage, SubPage

class PageAdmin(admin.ModelAdmin):
	pass

class SubPageAdmin(admin.ModelAdmin):
	list_display = ('long_name', 'position')

admin.site.register(ParentPage, PageAdmin)
admin.site.register(SubPage, SubPageAdmin)
