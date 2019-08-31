import uuid

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Method, Mock, Request, Status, UserPermission
from .views import replace_templates


class MockCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')
        Status(status_code=200, reason='OK', descriprion='test').save()

    def test_get(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.get('/mock/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_form.html')
        self.client.logout()

        response = self.client.get('/mock/new/')
        self.assertRedirects(response=response, expected_url='/login/?mock_form.html=/mock/new/')

    def test_post(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.post('/mock/new/',
                                    {
                                        'title': 'test_name',
                                        'status': '200',
                                        'response_body': 'test_body',
                                        'is_active': 'on'
                                    }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_list.html')
        self.assertEqual(True if Mock.objects.filter(title='test_name') else False, True)
        self.client.logout()

        response = self.client.post('/mock/new/')
        self.assertRedirects(response=response, expected_url='/login/?mock_form.html=/mock/new/')


class MockListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')

    def test_get(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.get('/mock/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_list.html')
        self.client.logout()

        response = self.client.get('/mock/list/')
        self.assertRedirects(response=response, expected_url='/login/?mock_list.html=/mock/list/')

    def test_post(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.post('/mock/list/')
        self.assertEqual(response.status_code, 405)


class MockEditViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')
        Status(status_code=200,
               reason='OK',
               descriprion='null',
               ).save()
        Mock(title='ex',
             status=Status.objects.get(status_code=200),
             response_body='null',
             is_active=True,
             user=User.objects.get(username='francisc'),
             ).save()

    def test_get(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.get('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 404)

        UserPermission(user=User.objects.get(username='francisc'),
                       mock=Mock.objects.get(title='ex'),
                       ).save()
        response = self.client.get('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_edit.html')
        self.client.logout()

        response = self.client.get('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertRedirects(response=response, expected_url='/login/?mock_edit.html=/mock/edit/' + str(
            Mock.objects.get(title='ex').mock_path))

    def test_post(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.post('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path),
                                    {
                                        'title': 'ex',
                                        'status': '200',
                                        'response_body': 'test_body',
                                        'is_active': 'on'
                                    }, follow=True)
        self.assertEqual(response.status_code, 404)

        UserPermission(user=User.objects.get(username='francisc'),
                       mock=Mock.objects.get(title='ex'),
                       ).save()
        response = self.client.post('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path),
                                    {
                                        'title': 'ex',
                                        'status': '200',
                                        'response_body': 'test_body',
                                        'is_active': 'on'
                                    }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_list.html')
        self.assertEqual(True if Mock.objects.filter(title='ex') else False, True)
        self.assertEqual(Mock.objects.get(title='ex').response_body, 'test_body')
        self.client.logout()

        response = self.client.post('/mock/edit/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertRedirects(response=response, expected_url='/login/?mock_edit.html=/mock/edit/' + str(
            Mock.objects.get(title='ex').mock_path))


class MockHistoryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')
        Status(status_code=200,
               reason='OK',
               descriprion='null',
               ).save()
        Mock(title='ex',
             status=Status.objects.get(status_code=200),
             response_body='null',
             is_active=True,
             user=User.objects.get(username='francisc'),
             ).save()

    def test_get(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 404)

        UserPermission(user=User.objects.get(username='francisc'),
                       mock=Mock.objects.get(title='ex'),
                       ).save()
        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mock_history.html')
        self.client.logout()

        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertRedirects(response=response, expected_url='/login/?mock_history.html=/mock/history/' + str(
            Mock.objects.get(title='ex').mock_path))

    def test_post(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.post('/mock/history/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 405)


class RequestInfoViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')
        Status(status_code=200,
               reason='OK',
               descriprion='null',
               ).save()
        Mock(title='ex',
             status=Status.objects.get(status_code=200),
             response_body='null',
             is_active=True,
             user=User.objects.get(username='francisc'),
             ).save()
        Method(method='GET').save()
        Request(mock=Mock.objects.get(title='ex'),
                method=Method.objects.get(method='GET'),
                host='test', port=80, path='test', scheme='test', body='', req_no=1,
                ).save()

    def test_get(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path) + '/' + str(
            Request.objects.get(req_no=1).req_path))
        self.assertEqual(response.status_code, 404)

        UserPermission(user=User.objects.get(username='francisc'),
                       mock=Mock.objects.get(title='ex'),
                       ).save()
        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path) + '/' + str(
            Request.objects.get(req_no=1).req_path))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'req_info.html')
        self.client.logout()

        response = self.client.get('/mock/history/' + str(Mock.objects.get(title='ex').mock_path) + '/' + str(
            Request.objects.get(req_no=1).req_path))
        self.assertRedirects(response=response, expected_url='/login/?req_info.html=/mock/history/' + str(
            Mock.objects.get(title='ex').mock_path) + '/' + str(Request.objects.get(req_no=1).req_path))

    def test_post(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)

        response = self.client.post('/mock/history/' + str(Mock.objects.get(title='ex').mock_path) + '/' + str(
            Request.objects.get(req_no=1).req_path))
        self.assertEqual(response.status_code, 405)


class MockViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')
        Status(status_code=200,
               reason='OK',
               descriprion='null',
               ).save()
        Mock(title='ex',
             status=Status.objects.get(status_code=200),
             response_body='null',
             is_active=True,
             user=User.objects.get(username='francisc'),
             ).save()
        Mock(title='ex2',
             status=Status.objects.get(status_code=200),
             response_body='null',
             is_active=False,
             user=User.objects.get(username='francisc'),
             ).save()
        Method(method='GET').save()
        Method(method='POST').save()

    def test_get(self):
        response = self.client.get('/mock/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'null')

        response = self.client.get('/mock/' + str(Mock.objects.get(title='ex2').mock_path))
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/mock/' + str(uuid.uuid4()))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post('/mock/' + str(Mock.objects.get(title='ex').mock_path))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'null')

        response = self.client.get('/mock/' + str(Mock.objects.get(title='ex2').mock_path))
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/mock/' + str(uuid.uuid4()))
        self.assertEqual(response.status_code, 404)


class TemplatesTestCase(TestCase):
    def setUp(self):
        self.request = type('testclass', (object,), {'headers': {'bau': 'miau'}})()

    def test(self):
        self.assertEqual(replace_templates(None, '<% seq %>', 2), '2')
        self.assertEqual(replace_templates(None, '<% seq%>', None), '<% seq%>')
        self.assertEqual(replace_templates(None, '<%seq %>', None), '<%seq %>')
        self.assertEqual(replace_templates(None, '<%seq%>', None), '<%seq%>')

        self.assertEqual(replace_templates(self.request, '<% bau %>', None), 'miau')
        self.assertEqual(replace_templates(self.request, '<% ceva %>', None), 'undefined')
