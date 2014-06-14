from django.contrib import admin

from mcmun.models import RegisteredSchool, AddDelegates, ScholarshipSchoolApp
from mcmun.tasks import regenerate_invoice, regenerate_add_invoice
from committees.models import CommitteeAssignment

class CommitteeInline(admin.StackedInline):
	model = CommitteeAssignment
	extra = 3

class RegisteredSchoolAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school_name', 'email', 'is_approved', 'num_delegates', 'amount_owed', 'get_amount_paid')
	list_filter = ('is_approved', 'use_online_payment')
	exclude = ('account',)
	inlines = [CommitteeInline]
	"""readonly_fields = (
		'school_name', 'first_time', 'how_you_hear', 'another_school',
		'other_method', 'first_name', 'last_name',
		'address', 'mail_address', 'city', 'province_state','postal_code',
		'advisor_phone', 'fax','country', 'country_1', 'country_2',
		'country_3', 'country_4', 'country_5', 'country_6', 'country_7',
		'country_8', 'country_9', 'country_10', 'committee_1', 'committee_2',
		'committee_3', 'committee_4', 'experience',
		'merchandise', 'num_delegates', 'disclaimer',
	)"""

	def re_invoice(self, request, queryset):
		for obj in queryset:
			id = obj.id
			is_approved = obj.is_approved
			if is_approved:
				regenerate_invoice(id)
		message = "invoice successfully sent"
		self.message_user(request, message)

	re_invoice.short_description = "Send invoice to selected schools"
	actions = ['re_invoice']


class AddDelegatesAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school', 'add_num_delegates', 'amount_owed_additional', 'get_add_amount_paid')
	list_filter = ('add_use_online_payment',)

	def re_invoice(self, request, queryset):
		for obj in queryset:
			add_id = obj.id
			school_id = obj.school_id
			regenerate_add_invoice(school_id, add_id)
		message = "invoice successfully sent"
		self.message_user(request, message)

	re_invoice.short_description = "Send invoice to selected schools"
	actions = ['re_invoice']

class ScholarshipSchoolAdmin(admin.ModelAdmin):
	list_display = ('school', 'application_uploaded', 'is_international')

admin.site.register(RegisteredSchool, RegisteredSchoolAdmin)
admin.site.register(AddDelegates, AddDelegatesAdmin)
admin.site.register(ScholarshipSchoolApp, ScholarshipSchoolAdmin)
