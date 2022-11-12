from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks, TaskRelationLabel
from users.models import Users


class LabelsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        u = Users.objects.create_user(username='testuser', password='12345')
        self.client.force_login(u)
        self.l1 = Labels.objects.create(name='test_label_1')
        Labels.objects.create(name='test_label_2')

    def test_label_db_creation(self):
        label = Labels.objects.create(name='test_label')
        self.assertEqual('test_label', label.name)

    def test_unique_label_name(self):
        with self.assertRaises(ValidationError):
            Labels.objects.create(name='test_label_1')

    def test_labels_list_view(self):
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(
            len(response.context['labels']),
            Labels.objects.count()
        )
        self.assertQuerysetEqual(
            response.context['labels'],
            Labels.objects.all()
        )

    def test_label_create_view(self):
        response = self.client.post(
            reverse('label_create'),
            {'name': "test_label_3"}
        )
        self.assertEqual(Labels.objects.last().name, "test_label_3")
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Labels.objects.count(), 3)

    def test_label_update_view(self):
        label = Labels.objects.last()
        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}),
            {'name': 'label_updated'})
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, "label_updated")
        self.assertRedirects(response, reverse('labels_list'))

    def test_label_delete_view(self):
        label = Labels.objects.last()
        response = self.client.get(
            reverse('label_delete', args=(label.id,)), follow=True
        )
        self.assertContains(response, 'Are you sure')
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertNotContains(response, 'label_delete', status_code=302)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Labels.objects.count(), 1)

    def test_task_with_label_delete(self):
        u = Users.objects.last()
        t = Tasks.objects.create(
            name='test_task',
            author=u,
            description='test_task_description',
            status=Statuses.objects.create(name='some'),
            executor=u
        )
        TaskRelationLabel.objects.create(
            task=t,
            label=self.l1,
        )

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.l1.id})
        )
        self.assertEqual(Labels.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
