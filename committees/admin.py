from django.contrib import admin
from django import forms
from committees.models import *


class CommitteeAssignmentAdmin(admin.ModelAdmin):
	list_display = ('school', 'committee', 'assignment', 'is_valid', 'unassigned')

class ScholarshipIndividualAdmin(admin.ModelAdmin):
	list_display = ('name_of_delegate', 'school', 'committee', 'is_uploaded')
	ordering = ['-scholarship_individual']

	def school(self, obj):
		return "%s" % obj.committee_assignment.school
	school.short_description = 'School'
	school.admin_order_field  = 'committee_assignment__school'

	def committee(self, obj):
		return "%s" % obj.committee_assignment.committee
	committee.short_description = 'Committee'
	committee.admin_order_field = 'committee_assignment__committee'

admin.site.register(Category)
admin.site.register(Committee)
admin.site.register(Committee_Dais)
admin.site.register(CommitteeBackgroundGuide)
admin.site.register(AdHocApplication)
admin.site.register(BRICSApplication)
admin.site.register(NixonApplication)
admin.site.register(WallStreetApplication)
admin.site.register(CommitteeAssignment, CommitteeAssignmentAdmin)
admin.site.register(ScholarshipIndividual, ScholarshipIndividualAdmin)
