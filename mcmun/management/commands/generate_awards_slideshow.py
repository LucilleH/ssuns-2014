import codecs
from collections import defaultdict
from operator import itemgetter
from xml.dom import minidom
from xml.etree.ElementTree import tostring

from django.core.management.base import BaseCommand, CommandError

from committees.models import AwardAssignment, Committee
from mcmun.models import RegisteredSchool as S


def get_highest_value(d):
    """Sort the dictionary by value and return the top entry's key."""
    return sorted(d.items(), key=itemgetter(1), reverse=True)[0][0]

def calculate_best_delegations():
    award_points = {
        'Best Delegate': 5,
        'Outstanding Delegate': 4,
        'Book Award': 3,
        'Honorable Mention': 1,
    }

    # Calculate the points, and the number of winners, for each school
    school_points = defaultdict(int)
    school_winners = defaultdict(int)
    for award in AwardAssignment.objects.filter(position__isnull=False):
        num_points = award_points[award.award.name]
        school = award.position.school
        school_points[school.school_name] += num_points
        school_winners[school.school_name] += 1

    # Figure out the totals for each school
    small_totals = {}
    large_totals = {}
    for school_name in school_points:
        num_points = school_points[school_name]
        num_winners = school_winners[school_name]
        num_delegates = S.objects.get(school_name=school_name).num_delegates
        total = (num_points + num_winners) / float(num_delegates)

        print school_name,
        print "%d points, %d winners, %d delegates; %.2f total" % (
            num_points, num_winners, num_delegates, total)

        if 2 <= num_delegates <= 15:
            small_totals[school_name] = total
            print "small delegation"
        elif num_delegates >= 16:
            large_totals[school_name] = total
            print "large delegation"

    # Sort them by value to find the best large and small delegations
    best_large = get_highest_value(large_totals)
    best_small = get_highest_value(small_totals)

    return best_large, best_small



class Command(BaseCommand):
    help = ("Generates the awards slideshow, as a PDF.")
    args = '[path to SVG file]'

    def handle(self, filename, *args, **options):
        # First, get all the committee data
        committees = Committee.objects.all()
        committees_dict = {}
        for committee in committees:
            committees_dict[committee.slug] = committee

        svg_file = open(filename)
        doc = minidom.parse(svg_file)
        for g in doc.lastChild.childNodes:
            if g.nodeName == 'g':
                label = g.getAttribute('inkscape:label')

                # Chop off the number and ! at the end to get the committee name
                # This is a really hacky workaround to using a regex
                if label.endswith('!'):
                    committee_name = label[:-2]

                    if committee_name in committees_dict:
                        committee = committees_dict[committee_name]
                        # Fill in the context dict (for string replacements)
                        awards = [award for award in committee.awards.order_by('award__name')]

                        # Move the outstanding one up, before book award
                        outstanding = awards.pop()
                        awards.insert(1, outstanding)
                        context = {}
                        print "-----------------------"
                        for i, award in enumerate(reversed(awards)):
                            print award.award
                            j = i + 1
                            if award.position:
                                delegate_name = award.position.assignment
                                school_name = award.position.school.school_name
                            else:
                                delegate_name = 'Wendy Liu'
                                school_name = 'McGill University'

                            context['award_name_%d' % j] = award.award.name
                            context['delegate_name_%d' % j] = delegate_name
                            context['school_name_%d' % j] = school_name

                        for flowPara in g.getElementsByTagName('flowPara'):
                            text = flowPara.firstChild
                            if text:
                                new_value = text.nodeValue % context
                                text.replaceWholeText(new_value)
                elif label.endswith('?'):
                    # The last 2 slides at the end, best large/small delegation
                    # Really hacky I know
                    #best_large, best_small = calculate_best_delegations()
                    best_large = 'best large'
                    best_small = 'best small'
                    print "Winners: %s (large) and %s (small)" % (best_large,
                        best_small)
                    context = {}
                    context['best_large'] = best_large
                    context['best_small'] = best_small

                    for flowPara in g.getElementsByTagName('flowPara'):
                        text = flowPara.firstChild
                        if text:
                            new_value = text.nodeValue % context
                            text.replaceWholeText(new_value)

                    continue
                else:
                    # Don't need to change anything, it's not a committee
                    continue

        # Save the updated SVG
        output_file = codecs.open('updated_awards.svg', 'w', encoding='utf-8')
        output_file.write(doc.toxml())
