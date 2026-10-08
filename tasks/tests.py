from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Task
class TaskTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('alice',password='Strong-demo-42!')
        self.other = get_user_model().objects.create_user('bob',password='Strong-demo-43!')
        self.task = Task.objects.create(owner=self.user,title='My task')
        self.foreign = Task.objects.create(owner=self.other,title='Private')
        self.client.force_login(self.user)
        self.api = APIClient(); self.api.force_authenticate(self.user)
    def test_html_crud(self):
        payload = {'title':'New task','description':'Details','status':'todo','priority':'high','due_date':'2026-12-01'}
        self.assertEqual(self.client.post('/tasks/new/',payload).status_code,302)
        item = Task.objects.get(title='New task')
        self.assertEqual(item.owner,self.user)
        self.assertEqual(self.client.get(f'/tasks/{item.pk}/').status_code,200)
        payload['title']='Updated'
        self.client.post(f'/tasks/{item.pk}/edit/',payload)
        item.refresh_from_db();self.assertEqual(item.title,'Updated')
        self.assertEqual(self.client.get(f'/tasks/{item.pk}/delete/').status_code,200)
        self.assertTrue(Task.objects.filter(pk=item.pk).exists())
        self.client.post(f'/tasks/{item.pk}/delete/')
        self.assertFalse(Task.objects.filter(pk=item.pk).exists())
    def test_html_owner_isolation(self):
        for suffix in ['', 'edit/', 'delete/']:
            self.assertEqual(self.client.get(f'/tasks/{self.foreign.pk}/{suffix}').status_code,404)
        self.assertEqual(self.client.post(f'/tasks/{self.foreign.pk}/delete/').status_code,404)
        self.assertNotContains(self.client.get('/'),'Private')
    def test_authentication(self):
        self.client.logout()
        self.assertEqual(self.client.get('/').status_code,302)
        self.assertIn(APIClient().get('/api/tasks/').status_code,[401,403])
    def test_api_crud_and_validation(self):
        self.assertEqual(self.api.post('/api/tasks/',{'title':''},format='json').status_code,400)
        r=self.api.post('/api/tasks/',{'title':'API task','status':'progress'},format='json')
        self.assertEqual(r.status_code,201);pk=r.data['id']
        self.assertEqual(self.api.patch(f'/api/tasks/{pk}/',{'status':'done'},format='json').data['status'],'done')
        self.assertEqual(self.api.get('/api/tasks/?status=done').data['count'],1)
        self.assertEqual(self.api.delete(f'/api/tasks/{pk}/').status_code,204)
    def test_api_owner_isolation(self):
        for method in ['get','patch','delete']:
            r=getattr(self.api,method)(f'/api/tasks/{self.foreign.pk}/')
            self.assertEqual(r.status_code,404)
        self.assertEqual(self.api.get('/api/tasks/').data['count'],1)
    def test_csrf_and_search(self):
        secure = Client(enforce_csrf_checks=True);secure.force_login(self.user)
        self.assertEqual(secure.post('/tasks/new/',{'title':'Blocked'}).status_code,403)
        self.assertContains(self.client.get('/?q=My'),'My task')
        self.assertNotContains(self.client.get('/?q=missing'),'My task')
