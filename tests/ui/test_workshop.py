import time

from django.core.files import File
from django.urls import reverse

from programdom.models import Workshop, Submission, Problem
from tests.ui.testcases import AuthedSplinterTestCase, WithBridgeTestCase


def make_submission():
    sub = Submission.objects.create(**{
        "pk": 1,
        "problem": Problem.objects.get(pk=1),
        "workshop": Workshop.objects.get(pk=1),
        "options": {"session_id": "0"},
        "code": File(open("tests/example_code.py", "rb"))
    })
    sub.save()
    return sub


class TestWorkshop(AuthedSplinterTestCase):

    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def test_create_workshop(self):
        url = f'{self.live_server_url}{reverse("workshop_new")}'
        self.browser.visit(url)
        self.browser.fill('title', 'New Test Workshop')
        self.browser.click_link_by_id("submit-id-submit")
        assert self.browser.find_by_tag("h3").first.value == "New Test Workshop"

        Workshop.objects.get(title="New Test Workshop").delete()

    def test_present_workshop_toggle(self):
        workshop = Workshop.objects.get(pk=1)
        workshop.end()
        url = f'{self.live_server_url}{reverse("workshop_present", kwargs={"pk":workshop.id})}'
        self.browser.visit(url)
        print(self.browser.find_by_tag("h3").first.value)
        assert self.browser.find_by_tag("h3").first.value == f"{workshop.title}"
        assert self.browser.find_by_id("btn_workshop_toggle").first.value == "Begin Workshop"
        self.browser.find_by_id("btn_workshop_toggle").first.click()
        workshop = Workshop.objects.get(pk=1)
        self.browser.find_by_value(workshop.code)


class TestWorkshopWS(WithBridgeTestCase):

    fixtures = ['workshops', "languages", "problems", "problem_tests"]
    reset_sequences = True


    def test_present_workshop_submissions(self):
        workshop = Workshop.objects.get(pk=1)
        workshop.start()
        url = f'{self.live_server_url}{reverse("workshop_present", kwargs={"pk":workshop.id})}'
        self.browser.visit(url)

        self.browser.find_by_css(".problem-button").first.click()
        sub = make_submission()
        time.sleep(5)
        passed = False
        for _ in range(5):
            if self.browser.evaluate_script("results_chart.data.datasets[0].data[0]") == 1:
                passed = True
                break
            time.sleep(1)
        assert passed
