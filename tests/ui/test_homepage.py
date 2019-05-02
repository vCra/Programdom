from django.urls import reverse

from tests.ui.testcases import AuthedSplinterTestCase

class TestHomepage(AuthedSplinterTestCase):

    def test_homepage_elements(self):
        url = f'{self.live_server_url}{reverse("home")}'
        self.browser.visit(url)
        assert len(self.browser.find_by_css(".card")) == 2

