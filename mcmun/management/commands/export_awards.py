import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from committees.models import AwardAssignment


class Command(BaseCommand):
    help = "Exports the awards for use in printing certificates."

    def handle(self, **options):
        field_names = [
            'Committee',
            'Position',
            'Delegatename',
            'University',
        ]
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
        writer.writerow(field_names)
        awards = AwardAssignment.objects.filter(award__name='Honorable Mention')
        for instance in awards:
            if instance.position is None:
	        continue

            row = [
                instance.committee.name,
                instance.position.assignment,
                instance.position.delegate_name,
                instance.position.school,
            ]
            writer.writerow([unicode(field).encode('utf-8') for field in row])
