from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class RegistrationTests(TestCase):
    def test_signup_creates_student_account_and_redirects_to_login(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newstudent',
                'email': 'newstudent@example.com',
                'first_name': 'New',
                'last_name': 'Student',
                'course': 'Computer Science',
                'password1': 'SafePassword!923',
                'password2': 'SafePassword!923',
            },
        )

        self.assertRedirects(response, reverse('login'))
        user = CustomUser.objects.get(username='newstudent')
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.assertEqual(user.course, 'Computer Science')
        self.assertTrue(user.check_password('SafePassword!923'))

    def test_signup_shows_success_message(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newstudent',
                'password1': 'SafePassword!923',
                'password2': 'SafePassword!923',
            },
            follow=True,
        )

        self.assertContains(response, 'Your account has been created.')

    def test_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newstudent',
                'password1': 'SafePassword!923',
                'password2': 'DifferentPassword!924',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='newstudent').exists())

    def test_login_dashboard_and_post_logout_flow(self):
        CustomUser.objects.create_user(
            username='newstudent',
            first_name='New',
            password='SafePassword!923',
            course='Computer Science',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'newstudent', 'password': 'SafePassword!923'},
        )

        self.assertRedirects(response, reverse('dashboard'))
        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertContains(dashboard_response, 'Welcome, New!')
        self.assertContains(dashboard_response, 'Computer Science')
        self.assertContains(dashboard_response, 'CampusConnect members')
        self.assertContains(dashboard_response, '>1</div>')
        self.assertNotContains(dashboard_response, reverse('admin_panel'))

        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 405)
        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('login'))
        self.assertRedirects(
            self.client.get(reverse('dashboard')),
            f"{reverse('login')}?next=/",
        )

    def test_student_cannot_access_admin_panel(self):
        student = CustomUser.objects.create_user(
            username='student',
            password='SafePassword!923',
        )
        self.client.force_login(student)

        self.assertEqual(self.client.get(reverse('admin_panel')).status_code, 403)

    def test_admin_can_access_admin_panel(self):
        admin = CustomUser.objects.create_user(
            username='admin',
            password='SafePassword!923',
            role=CustomUser.Role.ADMIN,
        )
        self.client.force_login(admin)

        self.assertContains(self.client.get(reverse('admin_panel')), 'Admin Panel')

    def test_superuser_is_shown_as_super_admin_and_can_access_admin_panel(self):
        superuser = CustomUser.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='SafePassword!923',
        )
        self.client.force_login(superuser)

        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertContains(dashboard_response, 'Super Admin dashboard')
        self.assertContains(dashboard_response, '>Super Admin</div>')
        self.assertContains(dashboard_response, reverse('admin_panel'))
        self.assertContains(self.client.get(reverse('admin_panel')), 'Admin Panel')

    def test_profile_update_edits_only_allowed_fields_for_signed_in_user(self):
        user = CustomUser.objects.create_user(
            username='student',
            first_name='Old',
            password='SafePassword!923',
            course='Old Course',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('profile'),
            {
                'first_name': 'Updated',
                'last_name': 'Student',
                'email': 'updated@example.com',
                'course': 'New Course',
                'role': CustomUser.Role.ADMIN,
                'is_superuser': 'on',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertContains(response, 'Your profile has been updated.')
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Student')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(user.course, 'New Course')
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.assertFalse(user.is_superuser)

    def test_profile_update_requires_login(self):
        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )
