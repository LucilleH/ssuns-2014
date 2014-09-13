import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.static import serve

from committees.models import Committee, position_paper_upload_path, scholarship_upload_path
from committees.utils import get_committee_from_email
from committees.forms import AwardAssignmentFormset


def view(request, slug):
	committee = get_object_or_404(Committee, slug=slug)
	# If the user is a member of the dais, show a link to the uploads page
	is_dais = get_committee_from_email(request.user.username) == committee

	show_manage_link = (committee.allow_manager(request.user) and committee.is_assignable)
	# If background guide is uploaded
	bgset = committee.committeebackgroundguide_set.all()
	bg_uploaded = False
	if bgset.count():
		bg_uploaded = True


	data = {
		'page': {
			'long_name': committee.name,
		},
		'is_dais': is_dais,
		'committee': committee,
		'bg_uploaded': bg_uploaded,
		'bgset': bgset,
		'show_manage_link': show_manage_link,
	}

	return render(request, 'committee.html', data)


def view_mobile(request, slug):
	committee = get_object_or_404(Committee, slug=slug)
	# If the user is a member of the dais, show a link to the uploads page
	# If background guide is uploaded
	bgset = committee.committeebackgroundguide_set.all()
	bg_uploaded = False
	if bgset.count():
		bg_uploaded = True


	data = {
		'page': {
			'long_name': committee.name,
		},
		'committee': committee,
		'bg_uploaded': bg_uploaded,
		'bgset': bgset,
	}

	return render(request, 'committee-mobile.html', data)




@login_required
def serve_papers(request, file_name):
	# Check if user is an admin/mod OR if the user uploaded the file OR dais
	is_authorised = False
	full_path = os.path.join(position_paper_upload_path, file_name)

	if request.user.is_staff:
		is_authorised = True
	elif request.user.username.endswith('@ssuns.org'):
		# Check the dais
		committee = get_committee_from_email(request.user.username)
		if committee and committee.committeeassignment_set.filter(position_paper=full_path):
			is_authorised = True
	else:
		user_schools = request.user.registeredschool_set.filter(is_approved=True)
		if user_schools.count() == 1:
			school = user_schools[0]
			if school.committeeassignment_set.filter(position_paper=full_path):
				is_authorised = True

	if is_authorised:
		return serve(request, file_name, os.path.join(settings.MEDIA_ROOT, position_paper_upload_path))
	else:
		raise PermissionDenied


@login_required
def list_papers(request, slug):
	committee = get_object_or_404(Committee, slug=slug)

	# Only the dais for this committee and other admins can access this
	if (get_committee_from_email(request.user.username) == committee
		or request.user.is_staff):
		data = {
			'page': {
				'long_name': 'Position papers for %s' % committee.name,
			},
			'committee': committee,
			'assignments': committee.committeeassignment_set.order_by('-position_paper'),
		}

		return render(request, 'list_papers.html', data)
	else:
		raise Http404

@login_required
def serve_scholarship(request, file_name):
	# Check if user is an admin/mod OR if the user uploaded the file OR dais
	is_authorised = False
	full_path = os.path.join(scholarship_upload_path, file_name)

	if request.user.is_staff:
		is_authorised = True
	elif request.user.username.endswith('@ssuns.org'):
                # Check the dais
		committee = get_committee_from_email(request.user.username)
		if committee and committee.committeeassignment_set.filter(position_paper=full_path):
			is_authorised = True
	else:
		user_schools = request.user.registeredschool_set.filter(is_approved=True)
		if user_schools.count() == 1:
			school = user_schools[0]
			if school.committeeassignment_set.filter(position_paper=full_path):
				is_authorised = True

	if is_authorised:
		return serve(request, file_name, os.path.join(settings.MEDIA_ROOT, scholarship_upload_path))
	else:
		raise PermissionDenied

@login_required
def list_scholarship(request):
	scholarship_list = []
	delegate_list = []
        # Only the dais for this committee and other admins can access this
        if (request.user.username.endswith('@ssuns.org') or request.user.is_staff):
                committee_list = Committee.objects.all()
		for committee in committee_list:
			assignment = committee.committeeassignment_set.all()
			for ass in assignment:
				scholarship = ass.scholarshipindividual_set.all()
				for scholar in scholarship:
					if scholar.scholarship_individual!="":
						scholarship_list.append(scholar)
						delegate_list.append(ass)
		data = {
                        'page': {
                                'long_name': 'scholarship list'
                        },
                        'scholarship_list': zip(delegate_list, scholarship_list),
                }

                return render(request, 'list_scholarship.html', data)
        else:
                raise Http404


@login_required
def manage(request, slug):
	committee = get_object_or_404(Committee, slug=slug)

	# Only the dais for this committee and other admins can access this
	if not committee.allow_manager(request.user):
		raise PermissionDenied

	assignments = committee.countrycharactermatrix_set.order_by('position')

	context = {
        'committee': committee,
        'title': 'Committee dashboard for %s' % committee.name,
        'assignments': assignments,
	}

	return render(request, 'committee_manage.html', context)


@login_required
def awards(request, slug):
	committee = get_object_or_404(Committee, slug=slug)
	if not committee.allow_manager(request.user):
		raise PermissionDenied

	awards = committee.awards.all()
	if request.method == 'POST':
		formset = AwardAssignmentFormset(request.POST, queryset=awards)
		if formset.is_valid():
			formset.save()
	else:
		formset = AwardAssignmentFormset(queryset=awards)

	context = {
        'committee': committee,
        'title': 'Awards dashboard for %s' % committee.name,
        'formset': formset,
        'positions': committee.countrycharactermatrix_set.all(),
	}

	return render(request, 'committee_awards.html', context)
