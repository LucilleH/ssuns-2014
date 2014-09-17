import os

from django.contrib.auth.models import User
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
	class Meta:
		ordering = ['name']

	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=20, unique=True)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category)
	assign_type = models.BooleanField(choices=ASSIGN_TYPE, verbose_name="Assignment Type")
	video_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="video URL")

	# The user (usually [slug]@mcmun.org) who can manage this committee.
	manager = models.ForeignKey(User, null=True, blank=True)

	class Meta:
		ordering = ('category', 'id')

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])

	def allow_manager(self, user):
		return self.manager == user or user.is_staff

	def is_searchable(self):
		return self.is_visible

	def get_num_delegates(self):
		return self.countrycharactermatrix_set.aggregate(
			total_delegates=models.Sum())['total_delegates']

	def allow_manager(self, user):
		return self.manager == user or user.is_staff

	def get_awards(self):
		awards = self.awards.order_by('award__name')
		# Move outstanding delegate to after best delegate
		# Should be fixed properly in the future (new field on Award)
		awards = [award for award in awards]
		outstanding = awards.pop()
		awards.insert(1, outstanding)
		return awards


	def __unicode__(self):
		return self.name
	
	def get_name(self):
		return self.name


	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])


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
	position = models.CharField(max_length=255)

	class Meta:
		unique_together = ('committee', 'position',)
		ordering = ('committee', 'position')
	
	def __unicode__(self):
		return "%s - %s" % (self.committee.name, self.position)


class CommitteeAssignment(models.Model):
	class Meta:
		ordering = ('school', 'assignment')
#		permissions = (("can_view_papers", "Can view position papers"),)

	# Number of delegates is usually 1, except in SOCHUM
	school = models.ForeignKey('mcmun.RegisteredSchool')
	# The country or character assignment
	committee = models.ForeignKey(Committee)
	assignment = models.CharField(max_length=255, choices=COUNTRIES_CHARACTER, null=True, blank=True)
	delegate_name = models.CharField(max_length=255, null=True, blank=True)
	position_paper = models.FileField(upload_to=get_position_paper_path, blank=True, null=True)

	def __unicode__(self):
		return "%s" % self.get_assignment_display()

	def is_filled(self):
		return self.delegate_name != ""

	def is_valid(self):
		return CommitteeAssignment.objects.filter(committee=self.committee, assignment=self.assignment).count() == 1
	is_valid.boolean = True

	def unassigned(self):
		num = int(self.school.num_delegates) - CommitteeAssignment.objects.filter(school=self.school).count()
		return "%s" % num

	def display_assignment(self):
		return "%s" % self.get_assignment_display()

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



class Award(models.Model):
	name = models.CharField(max_length=50)
	committees = models.ManyToManyField(Committee)

	def __unicode__(self):
		return self.name


class AwardAssignment(models.Model):
	award = models.ForeignKey(Award, related_name='assignments')
	committee = models.ForeignKey(Committee, related_name='awards')
	position = models.ForeignKey(CommitteeAssignment, null=True, blank=True)

	def __unicode__(self):
		return "%s in %s - %s" % (self.award, self.committee.name, self.position)

def update_award_assignments(sender, instance, action, reverse, *args,
    **kwargs):
	"""
	Defines an m2m_changed hook to create/remove AwardAssignments as necessary
	when the list valid committees for an Award is updated.
	"""
	if not reverse:
		if action == 'post_add':
			for committee in instance.committees.all():
				instance.assignments.get_or_create(committee=committee)
		elif action == 'pre_clear':
			instance.assignments.all().delete()

models.signals.m2m_changed.connect(update_award_assignments,
    sender=Award.committees.through)
