from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.urls import reverse
from tests.factory.user import AuthUserFactory


class AuthedSplinterTestCase(StaticLiveServerTestCase):


    def setUp(self):
        self.browser = Browser('chrome')
        user = AuthUserFactory()
        self.browser.visit(f'{self.live_server_url}{reverse("users:login")}')
        self.browser.fill('username', user.username)
        self.browser.fill('password', "password")
        self.browser.find_by_text("Login")[0].click()

    def tearDown(self):
        self.browser.quit()