from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users


class StatusesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        u = Users.objects.create_user(username='testuser', password='12345')
        self.client.force_login(u)
        self.s1 = Statuses.objects.create(name='test_status_1')
        Statuses.objects.create(name='test_status_2')

    def test_unique_status_name(self):
        with self.assertRaises(ValidationError):
            Statuses.objects.create(name='test_status_1')

    def test_statuses_list_view(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(
            len(response.context['statuses']),
            Statuses.objects.count()
        )
        self.assertQuerysetEqual(
            response.context['statuses'],
            Statuses.objects.all()
        )

    def test_status_create_view(self):
        response = self.client.post(
            reverse('status_create'),
            {'name': "test_status_3"}
        )
        self.assertEqual(Statuses.objects.last().name, "test_status_3")
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Statuses.objects.count(), 3)

    def test_status_update_view(self):
        status = Statuses.objects.last()
        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}),
            {'name': 'status_updated'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, "status_updated")
        self.assertRedirects(response, reverse('statuses_list'))

    def test_status_delete_view(self):
        status = Statuses.objects.last()
        response = self.client.get(
            reverse('status_delete', args=(status.id,)), follow=True
        )
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id})
        )
        self.assertNotContains(response, 'status_delete', status_code=302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Statuses.objects.count(), 1)

    def test_task_with_status_delete(self):
        u = Users.objects.last()
        Tasks.objects.create(
            name='test_task',
            author=u,
            description='test_task_description',
            status=self.s1,
            executor=u
        )

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': self.s1.id})
        )
        self.assertEqual(Statuses.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
