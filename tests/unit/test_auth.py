from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from tests.generators.user import AuthUserFactory


class TestViewAuthAnon(TestCase):
    """
    Tests that anon users are unable to view anything but the workshop_auth screen
    """

    user = AnonymousUser()
    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def test_workshop_auth(self):
        path = reverse("workshop_auth")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_list(self):
        path = reverse("workshop_list")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_new(self):
        path = reverse("workshop_new")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_detail(self):
        path = reverse("workshop_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_student_waiting(self):
        path = reverse("workshop_student_waiting", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_present(self):
        path = reverse("workshop_present", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_problems(self):
        path = reverse("workshop_problems", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    # Problem URLs

    def test_problem_list(self):
        path = reverse("problem_list")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_new(self):
        path = reverse("problem_create")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_detail(self):
        path = reverse("problem_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_delete(self):
        path = reverse("problem_delete", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_student(self):
        path = reverse("problem_student", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_test_new(self):
        path = reverse("problem_test_new", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_test_update(self):
        path = reverse("problem_test_update", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_test_delete(self):
        path = reverse("problem_test_delete", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302


class TestViewAuthStudent(TestCase):
    """
    Tests that anon users are unable to view anything but the workshop_auth screen
    """

    user = AnonymousUser()
    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def setUp(self):
        session = self.client.session
        session.update({"current_workshop_id": "abcdefgh"})
        session.save()

    def test_workshop_auth(self):
        path = reverse("workshop_auth")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_list(self):
        path = reverse("workshop_list")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_new(self):
        path = reverse("workshop_new")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_detail(self):
        path = reverse("workshop_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_student_waiting(self):
        path = reverse("workshop_student_waiting", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_present(self):
        path = reverse("workshop_present", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_workshop_problems(self):
        path = reverse("workshop_problems", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    # Problem URLs

    def test_problem_list(self):
        path = reverse("problem_list")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_new(self):
        path = reverse("problem_create")
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_detail(self):
        path = reverse("problem_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_delete(self):
        path = reverse("problem_delete", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_student(self):
        path = reverse("problem_student", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_test_new(self):
        path = reverse("problem_test_new", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_test_update(self):
        path = reverse("problem_test_update", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302

    def test_problem_test_delete(self):
        path = reverse("problem_test_delete", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 302


class TestViewAuthStaff(TestCase):
    """
    Tests that anon users are unable to view anything but the workshop_auth screen
    """

    fixtures = ['workshops', "languages", "problems", "problem_tests"]

    def setUp(self):
        user = AuthUserFactory()
        self.client.force_login(user)

    def test_workshop_auth(self):
        path = reverse("workshop_auth")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_list(self):
        path = reverse("workshop_list")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_new(self):
        path = reverse("workshop_new")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_detail(self):
        path = reverse("workshop_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_student_waiting(self):
        path = reverse("workshop_student_waiting", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_present(self):
        path = reverse("workshop_present", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_workshop_problems(self):
        path = reverse("workshop_problems", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    # Problem URLs

    def test_problem_list(self):
        path = reverse("problem_list")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_new(self):
        path = reverse("problem_create")
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_detail(self):
        path = reverse("problem_detail", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_delete(self):
        path = reverse("problem_delete", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_student(self):
        path = reverse("problem_student", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_test_new(self):
        path = reverse("problem_test_new", kwargs={"pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_test_update(self):
        path = reverse("problem_test_update", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200

    def test_problem_test_delete(self):
        path = reverse("problem_test_delete", kwargs={"pk": 1, "tc_pk": 1})
        response = self.client.get(path)
        assert response.status_code == 200
