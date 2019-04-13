from django.test import TestCase
from django.urls import reverse, resolve


class TestURLs(TestCase):

    # Workshop URLs

    def test_workshop_auth_url(self):
        path = reverse("workshop_auth")
        assert resolve(path).view_name == "workshop_auth"

    def test_workshop_list_url(self):
        path = reverse("workshop_list")
        assert resolve(path).view_name == "workshop_list"

    def test_workshop_new_url(self):
        path = reverse("workshop_new")
        assert resolve(path).view_name == "workshop_new"

    def test_workshop_detail_url(self):
        path = reverse("workshop_detail", kwargs={"pk": 1})
        assert resolve(path).view_name == "workshop_detail"

    def test_workshop_student_waiting_url(self):
        path = reverse("workshop_student_waiting", kwargs={"pk": 1})
        assert resolve(path).view_name == "workshop_student_waiting"

    def test_workshop_present_url(self):
        path = reverse("workshop_present", kwargs={"pk": 1})
        assert resolve(path).view_name == "workshop_present"

    def test_workshop_problems_url(self):
        path = reverse("workshop_problems", kwargs={"pk": 1})
        assert resolve(path).view_name == "workshop_problems"

    # Problem URLs

    def test_problem_list_url(self):
        path = reverse("problem_list")
        assert resolve(path).view_name == "problem_list"

    def test_problem_new_url(self):
        path = reverse("problem_create")
        assert resolve(path).view_name == "problem_create"

    def test_problem_detail_url(self):
        path = reverse("problem_detail", kwargs={"pk": 1})
        assert resolve(path).view_name == "problem_detail"

    def test_problem_delete_url(self):
        path = reverse("problem_delete", kwargs={"pk": 1})
        assert resolve(path).view_name == "problem_delete"

    def test_problem_student_url(self):
        path = reverse("problem_student", kwargs={"pk": 1})
        assert resolve(path).view_name == "problem_student"

    def test_problem_test_new_url(self):
        path = reverse("problem_test_new", kwargs={"pk": 1})
        assert resolve(path).view_name == "problem_test_new"

    def test_problem_test_update_url(self):
        path = reverse("problem_test_update", kwargs={"pk": 1, "tc_pk": 1})
        assert resolve(path).view_name == "problem_test_update"

    def test_problem_test_delete_url(self):
        path = reverse("problem_test_delete", kwargs={"pk": 1, "tc_pk": 1})
        assert resolve(path).view_name == "problem_test_delete"

