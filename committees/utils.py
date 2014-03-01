from committees.models import Committee


email_committee_map = {
	'whs@mcmun.org': 'whs',
	'congocrisis@mcmun.org': 'congo',
	'sochum@mcmun.org': 'sochum',
	'wipo@mcmun.org': 'wipo',
	'oic@mcmun.org': 'oic',
	'abcde@mcmun.org': 'abcde',
	'unhcr@mcmun.org': 'unhcr',
	'ogp@mcmun.org': 'ogp',
	'sms@mcmun.org': 'social-media',
	'dc@mcmun.org': 'dc-comics',
	'firstministers@mcmun.org': 'cfp',
	'culturalrev@mcmun.org': 'cultural-revolution',
	'plannord@mcmun.org': 'plan-nord',
	'icc@mcmun.org': 'icc',
	'brics@mcmun.org': 'brics',
	'wallstreet@mcmun.org': 'wall-street',
	'germanolympics@mcmun.org': 'german-olympics',
	'adhoc@mcmun.org': 'ad-hoc',
	'kgb@mcmun.org': 'kgb',
	'awocgov@mcmun.org': 'awoc',
	'cosanostra@mcmun.org': 'awoc',
	'unamir@mcmun.org': 'rwanda',
	'fpr@mcmun.org': 'rwanda',
	'far@mcmun.org': 'rwanda',
	'frost@mcmun.org': 'frost-nixon',
	'nixon@mcmun.org': 'frost-nixon',
}

def get_committee_from_email(email):
	slug = email_committee_map.get(email, None)
	if slug:
		return Committee.objects.get(slug=slug)
