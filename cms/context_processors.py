from cms.models import ParentPage

def menu(request):
	return {
		'pages': ParentPage.objects.all()
	}
