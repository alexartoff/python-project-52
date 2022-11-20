from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from statuses.models import Statuses
from tasks.models import Tasks
from users.models import Users


class UsersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        u = Users.objects.create_user(username='test_user', password='12345')
        self.client.login(username=u.username, password=u.password)
        Users.objects.create(
            username='test_username_one',
            password='test_password',
            first_name='test_first_name',
            last_name='test_last_name',
        )
        Users.objects.create(
            username='test_username_two',
            password='test_password',
            first_name='test_first_name',
            last_name='test_last_name',
        )

    def test_users_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(len(response.context['users']), Users.objects.count())
        self.assertQuerysetEqual(
            response.context['users'],
            Users.objects.all()
        )

    def test_unique_username(self):
        with self.assertRaises(ValidationError):
            Users.objects.create(
                username='test_username_one',
                password=' ',
                first_name=' ',
                last_name=' ',
            )

    def test_short_username(self):
        response = self.client.get(reverse('register_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')
        response = self.client.post(
            reverse('register_user'),
            {
                'username': 'bug',
                'first_name': 'test_user_first_name',
                'last_name': 'test_user_last_name',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertContains(response, 'is too short! minimum 4 symbols')
        self.assertNotEqual(response.status_code, 302)

    def test_user_register_view(self):
        response = self.client.get(reverse('register_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')

        response = self.client.post(
            reverse('register_user'),
            {
                'username': 'test_user_register_username',
                'first_name': 'test_user_register_first_name',
                'last_name': 'test_user_register_last_name',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        u = Users.objects.last()
        self.assertEqual(u.username, 'test_user_register_username')
        self.assertEqual(u.first_name, 'test_user_register_first_name')
        self.assertEqual(u.last_name, 'test_user_register_last_name')
        self.assertRedirects(response, reverse('user_login'))

    def test_user_login(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')

        u = Users.objects.last()
        response = self.client.post(
            reverse('user_login'),
            {
                'username': u.username,
                'password': u.password,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login'))

    def test_user_update_view(self):
        u = Users.objects.last()

        # last user can't update test_user (from setUp)
        response = self.client.get(reverse('user_update', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        # last user is logged on, now can update himself
        self.client.force_login(u)
        response = self.client.get(reverse('user_update', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update.html')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': u.id}),
            {
                'username': 'user_updated',
                'first_name': 'user_update_first_name',
                'last_name': 'user_update_last_name',
                'password1': '123qwe!@#',
                'password2': '123qwe!@#',
            }
        )
        self.assertEqual(response.status_code, 302)
        u.refresh_from_db()
        self.assertEqual(u.username, 'user_updated')
        self.assertEqual(u.first_name, 'user_update_first_name')
        self.assertEqual(u.last_name, 'user_update_last_name')
        self.assertTrue(u.check_password('123qwe!@#'))
        self.assertRedirects(response, reverse('index_page'))

    def test_user_delete_view(self):
        u = Users.objects.last()

        # last user can't delete test_user (from setUp)
        response = self.client.get(reverse('user_delete', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        # last user is logged on, now can delete himself
        self.client.force_login(u)
        response = self.client.get(reverse('user_delete', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='confirm_delete.html')

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': u.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 2)

    def test_user_with_task_delete(self):
        u = Users.objects.last()
        Tasks.objects.create(
            name='test_task_one',
            author=u,
            description='test_task_one_description',
            status=Statuses.objects.create(name='some'),
            executor=u,
        )
        tasks_qs = Tasks.objects.filter(author=u.id)

        # last user is logged on and has tasks, can't delete himself
        self.client.force_login(u)
        response = self.client.get(reverse('user_delete', kwargs={'pk': u.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='confirm_delete.html')

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': u.id})
        )
        self.assertTrue(tasks_qs)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 3)

    def test_no_permission_user_delete(self):
        u = Users.objects.last()
        response = self.client.get(
            reverse('user_delete', kwargs={'pk': u.id})
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Users.objects.count(), 3)
