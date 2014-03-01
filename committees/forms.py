from committees.models import AdHocApplication, BRICSApplication, NixonApplication, WallStreetApplication, \
	CommitteeAssignment, ScholarshipIndividual

from django import forms


class AdHocAppForm(forms.ModelForm):
	class Meta:
		model = AdHocApplication


class BRICSAppForm(forms.ModelForm):
	class Meta:
		model = BRICSApplication


class NixonAppForm(forms.ModelForm):
	class Meta:
		model = NixonApplication


class WallStreetAppForm(forms.ModelForm):
	class Meta:
		model = WallStreetApplication


CommitteeAssignmentFormSet = forms.models.modelformset_factory(CommitteeAssignment,
	fields=('delegate_name', 'position_paper',), extra=0)

ScholarshipIndividualFormset = forms.models.modelformset_factory(ScholarshipIndividual,
	fields=('scholarship_individual',), extra=0)
