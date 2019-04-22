from tests.ui.testcases import StudentSplinterTestCase
from django.urls import reverse


class TestStudentProblem(StudentSplinterTestCase):

    def test_wrong_problem_submission(self):
        self.browser.visit((f'{self.live_server_url}{reverse("problem_student", kwargs={"pk": 1})}'))
        assert not self.browser.find_by_text("Add 2 numbers together").is_empty()
        assert self.browser.find_by_id("p_stat_1").first.value == "Not submitted"
        assert self.browser.find_by_id("p_stat_1").first.value == "Not submitted"

        self.browser.click_link_by_id("btn-submit")

