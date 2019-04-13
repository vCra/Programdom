from django.urls import reverse

from programdom.models import Workshop
from tests.ui.testcases import AuthedSplinterTestCase


class TestWorkshop(AuthedSplinterTestCase):

    def test_create_workshop(self):
        url = f'{self.live_server_url}{reverse("workshop_new")}'
        self.browser.visit(url)
        self.browser.fill('title', 'New Test Workshop')
        self.browser.click_link_by_id("submit-id-submit")
        assert self.browser.find_by_tag("h3").first.value == "New Test Workshop"

        Workshop.objects.get(title="New Test Workshop").delete()

