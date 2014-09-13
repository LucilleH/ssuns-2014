import os

from decimal import Decimal
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

from mcmun.utils import generate_random_password
from mcmun.constants import * 
from mcmun.tasks import send_email, generate_invoice
from committees.models import Committee, ScholarshipIndividual

scholarshipschool_upload_path = 'scholarship/school/'

def get_scholarshipschool_upload_path(instance, filename):
	return os.path.join(scholarshipschool_upload_path, str(instance.id) + os.path.splitext(filename)[1])


# test
class RegisteredSchool(models.Model):
	class Meta:
		ordering = ['school_name']

	school_name = models.CharField(max_length=100, unique=True)
	first_time = models.BooleanField(choices=YESNO)
	how_you_hear = models.CharField(max_length=14, choices=HOWYOUHEAR, null=True, blank=True)
	another_school = models.CharField(max_length=100, null=True, blank=True)
	other_method = models.CharField(max_length=100, null=True, blank=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=100, unique=True)
	personal_email = models.EmailField(max_length=100, unique=True)
	delegate_name =  models.CharField(max_length=100)
	delegate_email = models.EmailField(max_length=100, unique=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	mail_address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	province_state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	advisor_phone = models.CharField(max_length=20)
	fax = models.CharField(max_length=20, null=True, blank=True)
	country = models.CharField(max_length=2, choices=COUNTRIESFULL)


	num_delegates = models.IntegerField(default=1, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES + 1)])
	amount_paid = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)

	# Needs a boolean field anyway to make the admin interface better
	is_approved = models.BooleanField(default=False, verbose_name="Approve school")

	# Committee preferences. SO BAD
	committee_1 = models.ForeignKey(Committee, limit_choices_to= (Q(assign_type=False)), related_name="school_1")
	committee_2 = models.ForeignKey(Committee, limit_choices_to= (Q(assign_type=False)), related_name="school_2")
	committee_3 = models.ForeignKey(Committee, limit_choices_to= (Q(assign_type=False)), related_name="school_3")
	committee_4 = models.ForeignKey(Committee, limit_choices_to= (Q(assign_type=False)), related_name="school_4")


	# Country preferences.
	country_1 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_2 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_3 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_4 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_5 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_6 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_7 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_8 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_9 = models.CharField(max_length=100, choices=COUNTRIESNGO)
	country_10 = models.CharField(max_length=100, choices=COUNTRIESNGO)

	experience = models.TextField(null=True, blank=True)
	mcgill_tours = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES + 1)])
	merchandise = models.BooleanField(choices=YESNO)
	disclaimer = models.BooleanField(choices=YESNO, default=True)
	account = models.ForeignKey(User, null=True)

	use_online_payment = models.BooleanField(choices=YESNO)
	use_priority = models.BooleanField(default=False)
	late_payment = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)

	def has_prefs(self):
		return (self.committee_1 or self.committee_2 or self.committee_3 or
			self.committee_4)


	def is_international(self):
		"""
		Checks if the institution is "international" (i.e. outside North America).
		"""
		return self.country != 'CA' and self.country != 'US'

	def get_payment_type(self):
		if self.use_priority:
			payment_type = 'priority'
		else:
			payment_type = 'regular'

		return payment_type

	def get_currency(self):
		"""
		Returns CAD if the institution is Canadian, USD otherwise.
		"""
		return 'CAD' if self.country == 'CA' else 'USD'

	def get_tour_fee(self):
		return (self.mcgill_tours * 2)

	def get_tour_fee_str(self):
		return "%.2f" % (self.mcgill_tours * 2)

	def get_late_fee(self):
		return "$%s" % self.late_payment

	def get_total_raw(self):
		return self.num_delegates * self.get_delegate_fee() + self.get_delegate_fee() + self.get_tour_fee() + float(self.late_payment)

	def get_total_convenience_fee(self):
		return "%.2f" % (self.get_total_raw() * 0.03)

	def add_convenience_fee(self, number):
		"""
		Incorporates a 3% convenience fee into the number given iff the school
		has selected online payment and has registered after Sept 1.
		"""
		if self.use_online_payment:
			return number * 1.03
		else:
			return number

	def get_delegate_fee(self):
		delegate_fee = 85 if self.use_priority else 90

		return delegate_fee

	def get_total_delegate_fee(self):
		return self.get_delegate_fee() * self.num_delegates

	def get_total_owed(self):
		return "%.2f" % (self.add_convenience_fee(self.get_total_raw()) - float(self.amount_paid))

	def get_amount_paid(self):
		return "$%s" % self.amount_paid

	def amount_owed(self):
		return "$%s" % self.get_total_owed()

	def send_success_email(self):
		# Send out email to user (receipt of registration)
		receipt_subject = 'Successful registration for SSUNS 2014'
		receipt_message_filename = 'registration_success'
		receipt_context = {
			'first_name': self.first_name,
			'school_name': self.school_name,
		}

		send_email.delay(receipt_subject, receipt_message_filename, [self.email], context=receipt_context)

		# Send out email to Charge, myself (link to approve registration)
		approve_subject = 'New registration for SSUNS'
		approve_message_filename = 'registration_approve'
		approve_context = {
			'first_name': self.first_name,
			'last_name': self.last_name,
			'school_name': self.school_name,
			'email': self.email,
			'admin_url': settings.ADMIN_URL,
			'school_id': self.id,
		}

		send_email.delay(approve_subject, approve_message_filename, [settings.IT_EMAIL, settings.CHARGE_EMAIL], context=approve_context)

	def send_invoice_email(self, username, password):
		print "about to delay the generate_invoice task"
		generate_invoice.delay(self.id, username, password)

	def has_unfilled_assignments(self):
		return any(not c.is_filled() for c in self.committeeassignment_set.all())

	def __unicode__(self):
		return self.school_name


class AddDelegates(models.Model):
	school = models.ForeignKey(RegisteredSchool, null=False)
	add_num_delegates = models.IntegerField(default=1, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)], verbose_name="additional number of delegates")
	add_mcgill_tours = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)], verbose_name="mcgill tours")
	add_use_online_payment = models.BooleanField(choices=YESNO)
	add_amount_paid = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2, verbose_name="amount paid")
	use_priority = models.BooleanField(default=False)
	late_payment = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)

	def get_add_tour_fee(self):
		return (self.add_mcgill_tours * 2)

	def get_add_tour_fee_str(self):
		return "%.2f" % (self.get_add_tour_fee())

	def get_delegate_fee(self):
		delegate_fee = 85 if self.use_priority else 90

		return delegate_fee
	
	def get_add_base_fee(self):
		return (self.add_num_delegates * self.get_delegate_fee() + self.get_add_tour_fee() + float(self.late_payment))

	def get_late_fee(self):
		return "$%s" % self.late_payment

	def get_add_total_convenience_fee(self):
		return "%.2f" % (self.get_add_base_fee()  * 0.03)

	def add_convenience_fee(self, number):
		"""
		Incorporates a 3% convenience fee into the number given iff the school
		has selected online payment and has registered after Sept 1.
		"""
		if self.add_use_online_payment:
			return number * 1.03
		else:
			return number

	def get_payment_type(self):
		if self.use_priority:
			payment_type = 'priority'
		else:
			payment_type = 'regular'
                return payment_type

	def get_add_total_delegate_fee(self):
		return self.add_num_delegates * self.get_delegate_fee()

	def get_add_total_owed(self):
		return "%.2f" % (self.add_convenience_fee(self.get_add_base_fee()) - float(self.add_amount_paid))

	def get_add_amount_paid(self):
		return "$%s" % self.add_amount_paid

	def amount_owed_additional(self):
		return "$%s" % self.get_add_total_owed()

	def __unicode__(self):
		return self.school.school_name


class ScholarshipSchoolApp(models.Model):
	school = models.OneToOneField(RegisteredSchool, primary_key=True)
	scholarship = models.FileField(upload_to=get_scholarshipschool_upload_path, blank=True, null=True, verbose_name="school scholarship application")
	
	def __unicode__(self):
		return self.school.school_name

	def application_uploaded(self):
		return self.scholarship != ""
	application_uploaded.boolean = True

	def is_international(self):
		if self.school.country != 'CA' and self.school.country != 'US':
			return True
		return False
	is_international.boolean = True

class MerchandiseApp(models.Model):
	class Meta:
		ordering = ('school', 'item')

	school = models.ForeignKey(RegisteredSchool)
	item = models.CharField(max_length=50, default='t-shirt')

	xs = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])
	s = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])
	m = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])
	l = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])
	xl = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])
	xxl = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES)])

	price = models.DecimalField(default=Decimal(50), max_digits=6, decimal_places=2)
	paid = models.BooleanField(default=False)

	def __unicode__(self):
		return self.school.school_name

	def get_total_price(self):
		return "%.2f" % ((self.xs + self.s + self.m + self.l + self.xl + self.xxl) * self.price)

	def get_xs_price(self):
		return "%.2f" % (self.xs * self.price)

	def get_s_price(self):
		return "%.2f" % (self.s * self.price)

	def get_m_price(self):
		return "%.2f" % (self.m * self.price)

	def get_l_price(self):
		return "%.2f" % (self.l * self.price)

	def get_xl_price(self):
		return "%.2f" % (self.xl * self.price)

	def get_xxl_price(self):
		return "%.2f" % (self.xxl * self.price)




@receiver(models.signals.pre_save, sender=RegisteredSchool, dispatch_uid="approve_schools")
def approve_schools(sender, instance, **kwargs):
	"""
	When a school is approved, create an account for it (with a random
	password) and send an email containing the login info as well as the
	invoice (attached as a PDF).
	"""
	if instance.is_approved and instance.account is None:
		# School does not have an account. Make one!
		password = generate_random_password()
		username = instance.email[:30]
		email = instance.email
		new_account = User.objects.create_user(username=username, password=password, email=email)

		instance.account = new_account

		instance.send_invoice_email(new_account.username, password)
