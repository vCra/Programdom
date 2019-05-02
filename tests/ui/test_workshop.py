import time

from django.urls import reverse

from programdom.models import Workshop
from tests.ui.testcases import AuthedSplinterTestCase


class TestWorkshop(AuthedSplinterTestCase):

    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def test_create_workshop(self):
        url = f'{self.live_server_url}{reverse("workshop_new")}'
        self.browser.visit(url)
        self.browser.fill('title', 'New Test Workshop')
        self.browser.click_link_by_id("submit-id-submit")
        assert self.browser.find_by_tag("h3").first.value == "New Test Workshop"

        Workshop.objects.get(title="New Test Workshop").delete()

    def test_present_workshop(self):
        workshop = Workshop.objects.get(pk=1)
        workshop.end()
        url = f'{self.live_server_url}{reverse("workshop_present", kwargs={"pk":workshop.id})}'
        self.browser.visit(url)
        assert self.browser.find_by_tag("h3").first.value == workshop.title
        assert self.browser.find_by_id("btn_workshop_toggle").first.value == "Begin Workshop"
        self.browser.find_by_id("btn_workshop_toggle").first.click()
        time.sleep(500)
        workshop = Workshop.objects.get(pk=1)

        assert self.browser.find_by_css(".workshop_code").first.value == workshop.code