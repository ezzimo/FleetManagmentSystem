from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import User


class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass", first_name="Test", last_name="User"
        )
        self.client.login(email="test@example.com", password="testpass")

    def test_dashboard_view(self):
        response = self.client.get(reverse("account:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard/dashboard.html")

    def test_edit_details_view(self):
        response = self.client.get(reverse("account:edit_details"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard/edit_details.html")

        # Test form submission
        response = self.client.post(reverse("account:edit_details"), {"first_name": "New", "last_name": "Name"})
        self.assertRedirects(response, reverse("account:dashboard"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

    def test_delete_user_view(self):
        response = self.client.get(reverse("account:delete_user"))
#Test that the UserEditForm correctly updates the user's details when valid data is submitted:
def test_usereditform_updates_user_details(self):
    # Set up test data
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpassword"
    )
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserEditForm(data=data, instance=user)
    
    # Check that the form is valid
    self.assertTrue(form.is_valid())
    
    # Save the form and check that the user's details were updated
    form.save()
    user.refresh_from_db()
    self.assertEqual(user.first_name, "Test")
    self.assertEqual(user.last_name, "User")
#Test that the UserEditForm displays errors when invalid data is submitted, such as an invalid email address or a password that is too short:
def test_usereditform_displays_errors_with_invalid_data(self):
    # Set up test data
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpassword"
    )
    data = {
        "username": "testuser",
        "email": "invalidemail",  # Invalid email
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserEditForm(data=data, instance=user)
    
    # Check that the form is invalid and displays the appropriate error message
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors["email"], ["Enter a valid email address."])
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password1": "short",  # Password too short
        "password2": "short",
    }
    form = UserEditForm(data=data, instance=user)
    
    # Check that the form is invalid and displays the appropriate error message
    self.assertFalse(form.is_valid())
    self.assertEqual(
        form.errors["password1"], ["This password is too short. It must contain at least 8 characters."]
    )
#Test that the PwdResetForm correctly sends a password reset email to the user when valid data is submitted:
def test_pwdresetform_sends_reset_email(self):
    # Set up test data
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpassword"
    )
    data = {"email": "test@example.com"}
    form = PwdResetForm(data=data)
    
    # Check that the
