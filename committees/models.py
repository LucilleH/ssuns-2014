import os

from django.db import models
from django import forms
from mcmun.constants import COUNTRIES
from committees.constants import ASSIGN_TYPE, COUNTRIES_CHARACTER

position_paper_upload_path = 'position-papers/'
scholarship_upload_path = 'scholarship/individual/'

def get_position_paper_path(instance, filename):
	return os.path.join(position_paper_upload_path, str(instance.id) + filename)

def get_scholarship_upload_path(instance, filename):
	return os.path.join(scholarship_upload_path, str(instance.id) + filename)



class Category(models.Model):
	class Meta:
		ordering = ['position']

	name = models.CharField(max_length=50)
	# Determines the ordering in the menu bar
	position = models.PositiveIntegerField(unique=True)	

	class Meta:
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name


class Committee(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=20, unique=True)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category)
	assign_type = models.BooleanField(choices=ASSIGN_TYPE, verbose_name="Assignment Type")
	video_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="video URL")

	def __unicode__(self):
		return self.name + " (" + self.get_assign_type_display() + ")"
	
	def get_name(self):
		return self.name


	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])

	class Meta:
		ordering = ('category', 'id')

class CommitteeDais(models.Model):
	class Meta:
		ordering = ['position']

	committee = models.ForeignKey(Committee)
	name = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	position = models.IntegerField(max_length=2, choices=[(i,i) for i in range(20)])
	pic_name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return "%s - %s" % (self.committee.name, self.name)


class CommitteeBackgroundGuide(models.Model):
	committee = models.ForeignKey(Committee)
	bg_name = models.CharField(max_length=255)
	bg_link = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.bg_name

	class Meta:
		ordering = ('committee', 'id')



#class CustomModelChoiceField(forms.ModelChoiceField):
#	def label_from_instance(self, obj):
#		return "%s (%s)" % (obj.name, obj.get_assign_type_display())


# position available for each committee, so make less mistake when assigning positions to delegates
class CountryCharacterMatrix(models.Model):
	committee = models.ForeignKey(Committee)
	position = models.CharField(max_length=100)

	class Meta:
    		unique_together = ('committee', 'position',)
	
	def __unicode__(self):
		return "%s - %s" % (self.committee.name, self.position)


class CommitteeAssignment(models.Model):
	class Meta:
		ordering = ('school', 'assignment')
        permissions = (("can_view_papers", "Can view position papers"),)

	# Number of delegates is usually 1, except in SOCHUM
	school = models.ForeignKey('mcmun.RegisteredSchool')
	# The country or character assignment
	assignment = models.OneToOneField(CountryCharacterMatrix)
	delegate_name = models.CharField(max_length=255, null=True, blank=True)
	position_paper = models.FileField(upload_to=get_position_paper_path, blank=True, null=True)

	def __unicode__(self):
		return "%s" % self.assignment.position

	def is_filled(self):
		return self.delegate_name != ""

	def unassigned(self):
		num = int(self.school.num_delegates) - CommitteeAssignment.objects.filter(school=self.school).count()
		return "%s" % num

	def display_assignment(self):
		return "%s" % self.assignment.position

class ScholarshipIndividual(models.Model):
	class Meta:
		unique_together = ('committee_assignment', 'scholarship_individual')

	committee_assignment = models.ForeignKey(CommitteeAssignment)
	scholarship_individual = models.FileField(upload_to=get_scholarship_upload_path, blank=True, null=True)

	def name_of_delegate(self):
		delegate = self.committee_assignment.delegate_name
		if delegate != "":
			return delegate
		else:
			return "Delegate not assigned yet"

	def is_uploaded(self):
		return self.scholarship_individual != ""
	is_uploaded.boolean = True

def create_scholarship_individual(sender, instance, created, **kwargs):
	"""
	Defines a post_save hook to create the right number of DelegateAssignments
	(with no delegate name specified) for each CommitteeAssignment
	"""
	if created:
		instance.scholarshipindividual_set.create()

models.signals.post_save.connect(create_scholarship_individual, sender=CommitteeAssignment)
