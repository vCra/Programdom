from django.test import TestCase

from tests.factory.workshop import EmptyWorkshopFactory


class TestModels(TestCase):

    def test_code_creation(self):
        workshop = EmptyWorkshopFactory()

        assert not workshop.active

        workshop.start()
        assert workshop.active
        assert len(workshop.code) == 8

        workshop.end()
        assert not workshop.active
        assert workshop.code is None
