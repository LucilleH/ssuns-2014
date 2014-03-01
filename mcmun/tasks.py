import codecs

from celery.task import task
from django.core.mail import EmailMessage
from django.db.models.loading import get_model
from django_xhtml2pdf.utils import generate_pdf
from django.conf import settings


@task
def send_email(subject, message_filename, recipients, context={}, attachment_filenames=[], bcc=[]):
	print "beginning of email task"

	message = codecs.open('mcmun/email/%s.txt' % message_filename, encoding='utf-8').read()

	if context:
		# If the context dictionary is defined, do the string formatting
		message = message % context

	email = EmailMessage(subject, message, to=recipients, bcc=bcc)

	for attachment_filename in attachment_filenames:
		print "attaching file"
		email.attach_file(attachment_filename)

	email.send()

	print "finished email task"


@task
def generate_invoice(school_id, username, password):
	print "starting the generate_invoice task"
	RegisteredSchool = get_model('mcmun', 'RegisteredSchool')
	school = RegisteredSchool.objects.get(pk=school_id)

	invoice_context = {
		'first_name': school.first_name,
		'school_name': school.school_name,
		'username': username,
		'password': password,
		'num_delegates': school.num_delegates,
		'payment_method': 'online payment' if school.use_online_payment else 'cheque',
		'payment_type': school.get_payment_type(),
		'total_balance': school.get_total_owed(),
		'currency': school.get_currency(),
	}

	# Send out an email to the user explaining that their account has been approved
	# CC myself just in case they forget the password or whatever
	invoice_subject = 'Invoice for SSUNS 2013'
	invoice_message_filename = 'invoice'

	invoice_id = 'SSUNS13' + str(school_id).zfill(3)

	pdf_context = {
		'invoice_id': invoice_id,
		'payment_type': school.get_payment_type(),
		'school': school,
	}

	# Generate the invoice PDF, save it under tmp/
	pdf_filename = 'mcmun/invoice/ssuns_invoice_%s.pdf' % invoice_id
	file = open(pdf_filename, 'wb')
	pdf = generate_pdf('pdf/invoice.html', file_object=file, context=pdf_context)
	file.close()

	attachment_filenames = [pdf_filename]

	send_email.delay(invoice_subject, invoice_message_filename, [school.email], context=invoice_context, bcc=[settings.IT_EMAIL, settings.CHARGE_EMAIL], attachment_filenames=attachment_filenames)

@task
def regenerate_invoice(school_id):
	print "starting the generate_invoice task"
	RegisteredSchool = get_model('mcmun', 'RegisteredSchool')
	school = RegisteredSchool.objects.get(pk=school_id)

	invoice_context = {
		'first_name': school.first_name,
		'school_name': school.school_name,
		'num_delegates': school.num_delegates,
		'payment_method': 'online payment' if school.use_online_payment else 'cheque',
		'payment_type': school.get_payment_type(),
		'total_balance': school.get_total_owed(),
		'currency': school.get_currency(),
	}

	# Send out an email to the user explaining that their account has been approved
	# CC myself just in case they forget the password or whatever
	invoice_subject = 'Invoice for SSUNS 2013'
	invoice_message_filename = 're-invoice'

	invoice_id = 'SSUNS13' + str(school_id).zfill(3)

	pdf_context = {
		'invoice_id': invoice_id,
		'payment_type': school.get_payment_type(),
		'school': school,
	}

	# Generate the invoice PDF, save it under tmp/
	pdf_filename = 'mcmun/invoice/ssuns_invoice_%s.pdf' % invoice_id
	file = open(pdf_filename, 'wb')
	pdf = generate_pdf('pdf/invoice.html', file_object=file, context=pdf_context)
	file.close()

	attachment_filenames = [pdf_filename]

	send_email.delay(invoice_subject, invoice_message_filename, [school.email], context=invoice_context, bcc=[settings.IT_EMAIL, settings.CHARGE_EMAIL], attachment_filenames=attachment_filenames)

@task
def regenerate_add_invoice(school_id, add_id):
	print "starting the generate_invoice task"
	RegisteredSchool = get_model('mcmun', 'RegisteredSchool')
	AddDelegates = get_model('mcmun', 'AddDelegates')
	school = RegisteredSchool.objects.get(pk=school_id)
	addDelegates = AddDelegates.objects.get(pk=add_id)

	invoice_context = {
		'first_name': school.first_name,
		'school_name': school.school_name,
		'num_delegates': addDelegates.add_num_delegates,
		'payment_method': 'online payment' if addDelegates.add_use_online_payment else 'cheque',
		'payment_type': school.get_payment_type(),
		'total_balance': addDelegates.get_add_total_owed(),
		'currency': school.get_currency(),
	}

	# Send out an email to the user explaining that their account has been approved
	# CC myself just in case they forget the password or whatever
	invoice_subject = 'Invoice for SSUNS 2013, addtional delegates'
	invoice_message_filename = 'add-invoice'

	invoice_id = 'SSUNS13' + str(add_id).zfill(3)

	pdf_context = {
		'invoice_id': invoice_id,
		'school': school,
		'addDelegates': addDelegates,
	}

	# Generate the invoice PDF, save it under tmp/
	pdf_filename = 'mcmun/addinvoice/ssuns_invoice_%s.pdf' % invoice_id
	file = open(pdf_filename, 'wb')
	pdf = generate_pdf('pdf/add-invoice.html', file_object=file, context=pdf_context)
	file.close()

	attachment_filenames = [pdf_filename]

	send_email.delay(invoice_subject, invoice_message_filename, [school.email], context=invoice_context, bcc=[settings.IT_EMAIL, settings.CHARGE_EMAIL], attachment_filenames=attachment_filenames)

