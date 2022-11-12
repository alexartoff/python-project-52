from django.test import TestCase
from django.test import Client
from django.urls import reverse

from statuses.models import Statuses
from tasks.models import Tasks
from users.models import Users


class TasksTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Users.objects.create_user(
            username='test_author',
            password='12345'
        )
        self.executor = Users.objects.create_user(
            username='test_executor',
            password='12345'
        )
        self.status = Statuses.objects.create(name='test_status')
        self.client.login(username='test_author', password='12345')
        Tasks.objects.create(
            name='test_task_one',
            author=self.author,
            description='test_task_one_description',
            status=self.status,
            executor=self.executor,
        )
        Tasks.objects.create(
            name='test_task_two',
            author=self.author,
            description='test_task_two_description',
            status=self.status,
            executor=self.executor,
        )

    def test_tasks_list_view(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(
            len(response.context['tasks_list']),
            Tasks.objects.count()
        )
        self.assertQuerysetEqual(
            response.context['tasks_list'],
            Tasks.objects.all()
        )

    def test_tasks_create_view(self):
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='create.html')

        response = self.client.post(
            reverse('add_task'),
            {
                'name': "test_task_add",
                'author': self.author,
                'description': 'test_task_add_description',
                'status': self.status.pk,
                'executor': self.executor.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        task = Tasks.objects.last()
        self.assertEqual(task.name, "test_task_add")
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.description, "test_task_add_description")
        self.assertEqual(task.status.name, self.status.name)
        self.assertEqual(task.executor.username, self.executor.username)
        self.assertRedirects(response, reverse('tasks_list'))

    def test_tasks_update_view(self):
        task = Tasks.objects.first()
        response = self.client.get(
            reverse('task_update', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update.html')

        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            {
                'name': 'task_updated',
                'description': 'task_description_updated',
                'status': task.status.pk,
                'executor': task.executor.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, "task_updated")
        self.assertEqual(task.description, "task_description_updated")
        self.assertRedirects(response, reverse('tasks_list'))

    def test_task_delete_view(self):
        task = Tasks.objects.last()
        response = self.client.get(
            reverse('task_delete', args=(task.id,)),
            follow=True
        )
        self.assertContains(response, 'Are you sure')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id})
        )
        self.assertNotContains(response, 'task_delete', status_code=302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Tasks.objects.count(), 1)
