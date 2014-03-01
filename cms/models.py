from django.db import models
import markdown
import os

class Page(models.Model):
	# Used in the URL and on the filesystem (no spaces)
	short_name = models.CharField(max_length=50, unique=True)
	# Used for the menu (lowercase), and as the page title
	long_name = models.CharField(max_length=50)
	# Will show the <h1> with the title AND the mini breadcrumbs navbar shit
	show_nav = models.BooleanField(default=True)
	# Will populate the {{ page.content }} variable in the template (custom or default)
	content = models.TextField(blank=True, null=True)
	# Set to true if you want to use a custom template (pages/[short_name].html)
	custom_template = models.BooleanField(default=False)
	# Set to true if you want to display as home page
	use_home = models.BooleanField(default=False)
	# specify the name of the picture that they wanna use for the icon in the parent page
	pagePic = models.CharField(max_length=50, blank=True, null=True)
	#whether to display titlepic or not
	titlePic = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.long_name

	@models.permalink
	def get_absolute_url(self):
		return ('cms.views.main', [self.short_name])

class ParentPage(Page):
	class Meta:
		ordering = ['position']

	# Determines the ordering in the menu bar
	position = models.PositiveIntegerField(unique=True)

class SubPage(Page):
	class Meta:
		ordering = ['parent', 'position']
		unique_together = ('position', 'parent')

	parent = models.ForeignKey(ParentPage, related_name="subpages")
	# Has to be defined here because, different "self"s etc
	position = models.PositiveIntegerField()
