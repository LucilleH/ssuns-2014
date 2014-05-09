import datetime
import os

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django_xhtml2pdf.utils import generate_pdf
from django.shortcuts import render, redirect
from django.views.static import serve

from committees.forms import CommitteeAssignmentFormSet, ScholarshipIndividualFormset
from committees.models import ScholarshipIndividual
from committees.utils import get_committee_from_email
from mcmun.forms import RegistrationForm, ScholarshipSchoolForm, CommitteePrefsForm
from mcmun.constants import MIN_NUM_DELEGATES, MAX_NUM_DELEGATES
from mcmun.models import RegisteredSchool, AddDelegates, ScholarshipSchoolApp, scholarshipschool_upload_path


def home(request):
	return render(request, "home.html")


def registration(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			# Simple spam-prevention technique
			if not request.POST.get('address', '').startswith('http://'):
				registered_school = form.save()
				registered_school.save()

				# Send emails to user, stysis, myself
				registered_school.send_success_email()

			data = {
				'page': {
					'long_name': 'Succcessful registration'
				}
			}

			return render(request, "registration_success.html", data)
	else:
		form = RegistrationForm()

	data = {
		'form': form,
		'page': {
			'long_name': 'Registration',
		},
		'min_num_delegates': MIN_NUM_DELEGATES,
		'max_num_delegates': MAX_NUM_DELEGATES,
	}

	return render(request, "registration.html", data)



@login_required
def dashboard(request):
	# If it's a dais member, redirect to that committee's position paper listing
	if request.user.username.endswith('@ssuns.org'):
		dais_committee = get_committee_from_email(request.user.username)
		if dais_committee:
			return redirect(dais_committee)

	form = None
	school = None
	scholarshipfile = None
	addDelegateList = None
	additional_pay = None

	if request.user.registeredschool_set.count():
		# There should only be one anyway (see comment in models.py)
		school = request.user.registeredschool_set.filter(is_approved=True)[0]
		
		additional_pay = AddDelegates.objects.filter(school=school)

		if ScholarshipSchoolApp.objects.filter(school=school).count() == 0:
			# show scholarship application form 
			if request.method == 'POST':
				form = ScholarshipSchoolForm(request.POST, request.FILES)

				if form.is_valid():
					scholarship_app = form.save(commit=False)
					scholarship_app.school = school
					scholarship_app.save()

					form = None
					scholarshipfile = ScholarshipSchoolApp.objects.get(school=school)
			else:
				form = ScholarshipSchoolForm()
		else:
			scholarshipfile = ScholarshipSchoolApp.objects.get(school=school)

		# If we haven't passed the committee prefs deadline, show the form
	elif request.user.is_staff:
		# Show a random school (the first one registered)
		# Admins can see the dashboard, but can't fill out any forms
		school = RegisteredSchool.objects.get(email="lucille.hua@gmail.com")

	com_assignments = school.committeeassignment_set.all()
	formset = CommitteeAssignmentFormSet(queryset=com_assignments, prefix='lol')
	scholar_forms = []
	for com_assignment in com_assignments:
		scholar_forms.append(ScholarshipIndividualFormset(queryset=com_assignment.scholarshipindividual_set.all(), prefix='%d' % com_assignment.id))

	data = {
		'management_forms': [formset.management_form] + [f.management_form for f in scholar_forms],
		'formset': zip(formset, scholar_forms),
		'unfilled_assignments': school.has_unfilled_assignments(),
		'school': school,
		'additional_pay': additional_pay,
		'scholarshipform': form,
		'scholarshipfile': scholarshipfile,
		# Needed to show the title (as base.html expects the CMS view)
		'page': {
			'long_name': 'Your dashboard',
		},
	}

	return render(request, "dashboard.html", data)


@login_required
def assignments(request):
	"""
	For updating assignments and handling position paper uploads
	"""
	user_schools = request.user.registeredschool_set.filter(is_approved=True)

	# Why ...
	if request.method == 'POST' and user_schools.count() == 1:
		school = user_schools[0]
		com_assignments = school.committeeassignment_set.all()
		formset = CommitteeAssignmentFormSet(request.POST, request.FILES, queryset=com_assignments, prefix='lol')
		formset.save()
		for com_ass in com_assignments:
			formset = ScholarshipIndividualFormset(request.POST, request.FILES, queryset=com_ass.scholarshipindividual_set.all(), prefix='%d' % com_ass.id)
			formset.save()

	return redirect(dashboard)


@login_required
def serve_scholarshipschool(request, file_name):
	# Check if user is an admin/mod OR if the user uploaded the file OR dais
	is_authorised = False
	full_path = os.path.join(scholarshipschool_upload_path, file_name)

	if request.user.is_staff:
		is_authorised = True
	elif request.user.username.endswith('@ssuns.org'):
		is_authorised = True
	else:
		user_schools = request.user.registeredschool_set.filter(is_approved=True)
		if user_schools.count() == 1:
			is_authorised = True

	if is_authorised:
		return serve(request, file_name, os.path.join(settings.MEDIA_ROOT, scholarshipschool_upload_path))
	else:
		raise PermissionDenied


def nikhil_error(request):
	# For testing errors
	raise SystemError
