from django.test import TestCase

from mcmun.models import RegisteredSchool as S


class SimpleTest(TestCase):
    def test_basic_addition(self):
        for s in S.objects.all():
            n = 0
            for c in s.committeeassignment_set.all():
                n += c.num_delegates
                if n > 0:
                    print s, n
