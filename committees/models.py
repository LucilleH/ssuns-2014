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
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name


class Committee(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=20, unique=True)
	description = models.TextField()
	category = models.ForeignKey(Category)
	assign_type = models.BooleanField(choices=ASSIGN_TYPE, verbose_name="Assignment Type")

	def __unicode__(self):
		return self.name + " (" + self.get_assign_type_display() + ")"
	
	def get_name(self):
		return self.name


	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])

	class Meta:
		ordering = ('category', 'id')

class Committee_Dais(models.Model):
	name = models.CharField(max_length=255)
	position = models.CharField(max_length=255)
	pic_name = models.CharField(max_length=255, unique=True)
	committee = models.ForeignKey(Committee)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('committee', 'id')

class CommitteeBackgroundGuide(models.Model):
	committee = models.ForeignKey(Committee)
	bg_name = models.CharField(max_length=255)
	bg_link = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.bg_name

	class Meta:
		ordering = ('committee', 'id')


class CommitteeApplication(models.Model):
	"""
	An abstract base class used by all committee applications
	"""
	class Meta:
		abstract = True

	name = models.CharField(max_length=100)
	school = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	head_delegate_name = models.CharField(max_length=100, verbose_name="Name of head delegate")
	field_of_study = models.CharField(max_length=100)
	previous_mun_experience = models.TextField(verbose_name="Describe your previous Model UN experience.")

	def __unicode__(self):
		return "%s for %s" % (self.name, self.committee_name)


class AdHocApplication(CommitteeApplication):
	# This is used solely for display. Can't actually use self.committee.
	committee_name = 'the Ad-Hoc Committee of the Secretary-General'

	what_topic = models.TextField(verbose_name="If you were given the opportunity to select the Ad-Hoc committee topic, what topic would you choose?")
	world_leader_coffee = models.TextField(verbose_name="Who is one living world leader you would like to have a coffee talk with and why?")
	no_background_knowledge = models.TextField(verbose_name="What will you do if you have no background knowledge of the chosen topic?")
	# There must be a better way to do this?
	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)


class BRICSApplication(CommitteeApplication):
	committee_name = 'the BRICS Summit'

	teammate_1_name_email = models.CharField(max_length=255, verbose_name="Name and email of teammate 1")
	teammate_2_name_email = models.CharField(max_length=255, verbose_name="Name and email of teammate 2")
	what_topic = models.TextField(verbose_name="What would you choose as the BRICS Summit topic of discussion and why?")
	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)
	world_leader_coffee = models.TextField(verbose_name="Who is one living world leader you would like to have a coffee talk with and why?")
	significance_of_brics = models.TextField(verbose_name="Describe the significance of the BRICS nations in less than 250 words.")


class NixonApplication(CommitteeApplication):
	committee_name = "the Nixon Interviews Joint Crisis"

	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)
	significance = models.TextField(verbose_name="What is the significance of the interviews held between David Frost and Richard Nixon?")
	which_side = models.TextField(verbose_name="Which side of the joint crisis would you prefer to be on and why?")
	frost_ask_nixon = models.TextField(verbose_name="If you were David Frost, what would you have asked Richard Nixon?")
	nixon_presidency = models.TextField(verbose_name="Describe Richard Nixon's presidency in less than 250 words.")


class WallStreetApplication(CommitteeApplication):
	committee_name = "Wall Street 2008"

	facebook_ipo = models.TextField(verbose_name="In May 2012, Facebook, Inc. held its initial public offering (IPO) at an unprecedented valuation for an internet corporation. Since then, it is arguable that Facebook's IPO failed to match traders' expectations. Do you agree? Also, what are the long-term and the short-term forecasts for Facebook's stock in your opinion? Explain in less than two hundred words.")
	british_libor = models.TextField(verbose_name="This summer, the British financial system faced heavy scrutiny and damaging accusations of manipulation of the London Interbank Offered Rate (LIBOR). Should the British government get involved? What are the implications of this scandal? Explain in less than two hundred words.")
	bull_bear = models.TextField(verbose_name="Are you bull-ish or bear-ish? Explain in two sentences or less.")



class CustomModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s (%s)" % (obj.name, obj.get_assign_type_display())


class CommitteeAssignment(models.Model):
	class Meta:
		ordering = ('school', 'committee')
        permissions = (("can_view_papers", "Can view position papers"),)

	# Number of delegates is usually 1, except in SOCHUM
	school = models.ForeignKey('mcmun.RegisteredSchool')
	committee = models.ForeignKey(Committee)
	# The country or character name, in plain text
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
