from committees.models import *

from django import forms



CommitteeAssignmentFormSet = forms.models.modelformset_factory(CommitteeAssignment,
	fields=('delegate_name', 'position_paper',), extra=0)

ScholarshipIndividualFormset = forms.models.modelformset_factory(ScholarshipIndividual,
	fields=('scholarship_individual',), extra=0)

AwardAssignmentFormset = forms.models.modelformset_factory(AwardAssignment,
    fields=('position',), extra=0)
