from django.contrib import admin
from django import forms
from committees.models import *
from committees.constants import COUNTRYLIST

class CCMInline(admin.StackedInline):
	model = CountryCharacterMatrix
	extra = 3

class CommitteeAdmin(admin.ModelAdmin):
	ordering = ['name']
	inlines = [CCMInline]

	def assign_countries(self, request, queryset):
		for obj in queryset:
			for country in COUNTRYLIST:
				CountryCharacterMatrix.objects.get_or_create(committee=obj, position=country)

		message = "country matrix created"
		self.message_user(request, message)
	assign_countries.short_description = "Insert all countries to CCM for selected committees"
	actions=['assign_countries']


class CommitteeAssignmentAdmin(admin.ModelAdmin):
	list_display = ('school', 'assignment','delegate_name', 'unassigned')

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


class CommitteeDaisAdmin(admin.ModelAdmin):
	ordering = ['committee']

admin.site.register(Category)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(CommitteeDais, CommitteeDaisAdmin)
admin.site.register(CommitteeBackgroundGuide)
admin.site.register(CountryCharacterMatrix)
admin.site.register(CommitteeAssignment, CommitteeAssignmentAdmin)
admin.site.register(ScholarshipIndividual, ScholarshipIndividualAdmin)
