from committees.models import CommitteeAssignment, ScholarshipIndividual

from django import forms



CommitteeAssignmentFormSet = forms.models.modelformset_factory(CommitteeAssignment,
	fields=('delegate_name', 'position_paper',), extra=0)

ScholarshipIndividualFormset = forms.models.modelformset_factory(ScholarshipIndividual,
	fields=('scholarship_individual',), extra=0)
