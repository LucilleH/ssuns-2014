from django.contrib import admin
from django import forms
from committees.models import *
from committees.constants import COUNTRYLIST

class CommitteeAdmin(admin.ModelAdmin):
	ordering = ['name']


class CommitteeAssignmentAdmin(admin.ModelAdmin):
	list_display = ('school', 'committee', 'assignment','delegate_name','is_valid', 'unassigned')
	ordering = ['school', 'assignment',]

class ScholarshipIndividualAdmin(admin.ModelAdmin):
	list_display = ('name_of_delegate', 'school', 'committee_assignment', 'is_uploaded')
	ordering = ['-scholarship_individual']

	def school(self, obj):
		return "%s" % obj.committee_assignment.school
	school.short_description = 'School'
	school.admin_order_field  = 'committee_assignment__school'

	def committee(self, obj):
		return "%s" % obj.committee_assignment.committee
	committee.short_description = 'Committee'
	committee.admin_order_field = 'committee_assignment'

class CountryCharacterMatrixAdmin(admin.ModelAdmin):
	ordering = ['committee', 'position',]

class CommitteeDaisAdmin(admin.ModelAdmin):
	ordering = ['committee']

class AwardAssignmentAdmin(admin.ModelAdmin):
	list_display = ('position', 'award', 'committee', 'school')
	list_per_page = 112  # show all the awards on one page

	def school(self, obj):
		if obj.position:
			return "%s" % obj.school
		else:
			return "(None)"
	school.short_description = 'School'
	school.admin_order_field  = 'position__school'


admin.site.register(Category)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(CommitteeDais, CommitteeDaisAdmin)
admin.site.register(CommitteeBackgroundGuide)
admin.site.register(CountryCharacterMatrix, CountryCharacterMatrixAdmin)
admin.site.register(CommitteeAssignment, CommitteeAssignmentAdmin)
admin.site.register(ScholarshipIndividual, ScholarshipIndividualAdmin)
admin.site.register(Award)
admin.site.register(AwardAssignment, AwardAssignmentAdmin)
