from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings

from commons.test.base import BaseAPITestCase
from commons.test.decorators import login
from surveys.models import Survey
from surveys.serializers import SurveySerializer


class SurveyViewSetTest(BaseAPITestCase):
    fixtures = ['surveys', 'users']

    list_url_pattern = 'surveys:survey-list'
    detail_url_pattern = 'surveys:survey-detail'

    data = {
        'name': 'ZXC',
        'description': 'Zed eX Ci',
        'created_at': '2021-03-15T08:00:00.000Z',
        'start_at': '2021-03-17T18:00:00.000Z',
        'end_at': '2021-03-19T18:00:00.000Z',
    }

    @login('admin')
    def setUp(self) -> None:
        super().setUp()

    def test_list(self):
        response = self.client.get(reverse(self.list_url_pattern))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), min(Survey.objects.count(), api_settings.PAGE_SIZE))

    def test_create(self):
        response = self.client.post(reverse(self.list_url_pattern), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('name'), self.data['name'])

    def test_retrieve(self):
        response = self.client.get(reverse(self.detail_url_pattern, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), Survey.objects.get(pk=1).name)

    def test_update(self):
        response = self.client.put(reverse(self.detail_url_pattern, args=[1]), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), self.data['name'])

    def test_partial_update(self):
        response = self.client.patch(reverse(self.detail_url_pattern, args=[1]), data={'name': 'sas'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'sas')

    def test_delete(self):
        self.client.delete(reverse(self.detail_url_pattern, args=[1]))
        self.assertFalse(Survey.objects.filter(pk=1).exists())


class SurveySerializerTest(TestCase):
    def test_validate(self):
        serializer = SurveySerializer()
        self.assertRaises(ValidationError, serializer.validate, {
            'name': 'ZXC',
            'description': 'Zed eX Ci',
            'created_at': '2021-03-15T08:00:00.000Z',
            'start_at': '3333-33-33T18:00:00.000Z',
            'end_at': '2222-22-22T18:00:00.000Z',
        })  # start_at is later than end_at
