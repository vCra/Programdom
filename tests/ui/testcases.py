import os
import subprocess
from sys import stdout, stderr

from channels.testing import ChannelsLiveServerTestCase
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.cache import cache
from splinter import Browser
from django.urls import reverse

from programdom.models import Workshop
from tests.generators.user import AuthUserFactory

HEADLESS = settings.HEADLESS

class AuthedSplinterTestCase(ChannelsLiveServerTestCase):


    def setUp(self):
        self.browser = Browser('chrome', headless=True)

        user = AuthUserFactory()
        self.browser.visit(f'{self.live_server_url}{reverse("users:login")}')
        self.browser.fill('username', user.username)
        self.browser.fill('password', "password")
        self.browser.find_by_text("Login")[0].click()

    def tearDown(self):
        self.browser.quit()


class StudentSplinterTestCase(ChannelsLiveServerTestCase):

    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def setUp(self):
        self.browser = Browser('chrome', headless=True)
        self.browser.visit(f'{self.live_server_url}{reverse("workshop_auth")}')
        self.workshop = Workshop.objects.get(pk=1)
        self.workshop.start()
        self.browser.fill('code', self.workshop.code)
        self.browser.click_link_by_id("submit-id-submit")

    def tearDown(self):
        self.browser.quit()


class WithBridgeTestCase(AuthedSplinterTestCase):

    bridge_process = None

    def setUp(self):
        cache.clear()
        super().setUp()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        env = os.environ.copy()
        env["DATABASE_URL"] = "postgresql://postgres@localhost:5432/" + settings.DATABASES['default']['NAME']

        cls.bridge_process = subprocess.Popen(["python", "manage.py", "runworker", "judgebridge"], env=env)
        cls.bridge_process.stdout = stdout
        cls.bridge_process.stderr = stderr
    @classmethod
    def tearDownClass(cls):
        cls.bridge_process.terminate()
        super().tearDownClass()
