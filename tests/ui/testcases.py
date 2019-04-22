import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.urls import reverse

from programdom.models import Workshop
from tests.factory.user import AuthUserFactory


class AuthedSplinterTestCase(StaticLiveServerTestCase):


    def setUp(self):
        self.browser = Browser('chrome', headless=True)

        user = AuthUserFactory()
        self.browser.visit(f'{self.live_server_url}{reverse("users:login")}')
        self.browser.fill('username', user.username)
        self.browser.fill('password', "password")
        self.browser.find_by_text("Login")[0].click()

    def tearDown(self):
        self.browser.quit()


class StudentSplinterTestCase(StaticLiveServerTestCase):

    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def setUp(self):
        self.browser = Browser('chrome')
        self.browser.visit(f'{self.live_server_url}{reverse("workshop_auth")}')
        self.workshop = Workshop.objects.get(pk=1)
        self.workshop.start()
        self.browser.fill('code', self.workshop.code)
        self.browser.click_link_by_id("submit-id-submit")

    def tearDown(self):
        self.browser.quit()
