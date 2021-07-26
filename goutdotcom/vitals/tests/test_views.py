from django.apps import apps
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.vitals.models import Weight
from goutdotcom.vitals.tests.factories import WeightFactory

from ..views import VitalDetail

class TestDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.weight = WeightFactory()
        self.detail_url = reverse('vitals:detail', kwargs={'vital':self.weight.name, 'pk':self.weight.pk})

    def test_detail(self):
        ### request detail_url from reverse on fake Weight object above
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        response = VitalDetail.as_view()(request, vital=self.weight.name, pk=self.weight.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset(self):
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        view = VitalDetail(kwargs={'vital':self.weight.name, 'pk':self.weight.pk})
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(queryset, Weight.objects.filter(pk=self.weight.pk))
