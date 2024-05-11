from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from http import HTTPStatus
from pathlib import Path
from urllib.parse import urlencode
import io
import time

from main.models import Submission, CustomUser, File
from main.forms import LoginForm, CustomUserCreationForm, SubmissionForm
from .views import login_view, profile_view, index, reviewreports_view, delete_submission

#  form = CustomUserCreationForm(data={"username": "test_user1","email": "testing1@gmail.com","password": "Testing123!"})

# class UserLoginTests(TestCase):
#     def test_custom_user_invalid_credentials(self):
#         response = self.client.post("/login", data={"username": "testNotRealUser", "password": "Testing123!","email": "testFakeEmail@gmail.com"})
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertContains(response, 'Invalid username or password', html=True)

#wrapper for adding committed attribute to file
# class TestIOTextWrapper:
#     def __init__(self, wrapped_file):
#         self._wrapped_file = wrapped_file
#         self._committed = False

#     def __getattr__(self, name):
#         return getattr(self._wrapped_file, name)

#     @property
#     def committed(self):
#         return self._committed

#     @committed.setter
#     def committed(self, value):
#         self._committed = value

# class SubmissionTests(TestCase): // old submission model tests
#     def test_submission_model_with_file(self):
#         main_folder = Path(__file__).parent
#         path = main_folder / "test_text_file.txt"
#         test_file = open(path,'r')
#         test_text = test_file.read()
#         wrapped_test_file = TestIOTextWrapper(test_file)
#         wrapped_test_file.committed = True
#         test_submission = Submission.objects.create(username="testUser",file=wrapped_test_file,text=test_text)
#         result = Submission.objects.filter(username="testUser")
#         self.assertTrue(result,result.exists())

#     def test_submission_model_no_file(self):
#         Submission.objects.create(username="testUser",file=None)
#         result = Submission.objects.filter(username="testUser")
#         self.assertTrue(result,result.exists())

class CustomUserTests(TestCase):
    def setUp(self):
        CustomUser.objects.create(username="testUser", password="Testing123!", email="test@testing.com") #no site_admin specified, testing default=false call in model
    
    def test_custom_user_model(self):
        test_user = CustomUser.objects.get(username="testUser")
        self.assertEqual(test_user.username, "testUser")
        self.assertEqual(test_user.password, "Testing123!")
        self.assertEqual(test_user.email, "test@testing.com")
        self.assertFalse(test_user.site_admin)


class SubmissionTests(TestCase):
    def test_submission_model(self):
        Submission.objects.create(
            subject="test submission",
            text="test submission text"
        )
        result = Submission.objects.get(subject="test submission")
        self.assertEqual(result.text, "test submission text")
        self.assertEqual(result.status, "New")
        self.assertEqual(result.tag, "Other")
        self.assertEqual(result.admin_response, "N/A")


class FileTests(TestCase):
    def test_file_model(self):
        Submission.objects.create(
            subject="file test submission",
            text="file test submission text"
        )
        File.objects.create(
            submission=Submission.objects.get(subject="file test submission"),
            file=SimpleUploadedFile("test-file.txt",b"test file contents")
        )
        result = File.objects.filter(submission=Submission.objects.get(subject="file test submission"))
        self.assertTrue(result.exists())


class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(
            username="View-Testing-User",
            email="tester@views.test",
            password="password"
        )
        Submission.objects.create(
            subject="view test submission",
            text="view test submission text",
            user=CustomUser.objects.get(username="View-Testing-User")
        )
    def test_profile_page(self):
        request = self.factory.get("/profile")
        request.user = self.user
        response = profile_view(request)
        #Confirms that associated report is visible on user profile screen
        self.assertGreaterEqual(response.content.index(b"view test submission"), 0)
    def test_home_page(self):
        request = self.factory.get("/")
        request.user = self.user
        response = index(request)
        #Confirms that home page displays username of logged in user
        self.assertGreaterEqual(response.content.index(b"View-Testing-User"), 0)
    def test_review_reports(self):
        self.user = CustomUser.objects.create(
            username="test-admin",
            email="admin@view.test",
            password="password",
            site_admin=True
        )
        request = self.factory.get("/reviewreports")
        request.user = self.user
        response = reviewreports_view(request)
        #Confirms that report made in setUp() is visible on admin review report screen
        self.assertGreaterEqual(response.content.index(b"view test submission"), 0)
    def test_submission_delete(self):
        request = self.factory.post("/profile")
        request.user = self.user
        response = delete_submission(request, Submission.objects.get(subject="view test submission").pk)
        self.assertGreaterEqual(response.content.index(b"Submission Deleted!"), 0)

class FormTests(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username="test-login",
            email="test@login.test",
            password="password",
        )
    def test_login_form(self):
        form_data = {'username': 'test-login', 'password': 'password'}
        form = LoginForm(data=form_data)
        #Confirm that login form accepts the given data
        self.assertTrue(form.is_valid)
    def test_custom_user_form(self):
        form_data = {'username': 'test-form', 'password': 'password', 'email': 'form@form.test'}
        form = CustomUserCreationForm(data=form_data)
        #Confirm that custom user form accepts given data
        self.assertTrue(form.is_valid)
    def test_submission_form(self):
        form_data = {'subject': 'submission form test',
                    'text': 'submission form test text',
                    'tag': 'Cheating - Exam',
                    }
        form = SubmissionForm(data=form_data)
        #Confirm that submission form accepts given data
        self.assertTrue(form.is_valid)




