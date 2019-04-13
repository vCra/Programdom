from django.test import TestCase

from programdom.models import Workshop


class WorkshopTest(TestCase):
    def setUp(self):
        self.workshop = Workshop(title="Example Workshop")



