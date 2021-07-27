from django.apps import apps
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.users.tests.factories import UserFactory
from goutdotcom.vitals.models import Weight
from goutdotcom.vitals.tests.factories import WeightFactory

from ..views import IndexView, VitalDetail

class TestDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.weight = WeightFactory(user=self.user)
        self.detail_url = reverse('vitals:detail', kwargs={'vital':self.weight.name, 'pk':self.weight.pk})

    def test_detail(self):
        ### request detail_url from reverse on fake Weight object above
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        response = VitalDetail.as_view()(request, vital=self.weight.name, pk=self.weight.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_object(self):
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        view = VitalDetail(kwargs={'vital':self.weight.name, 'pk':self.weight.pk})
        view.model = apps.get_model('vitals', model_name=view.kwargs['vital'])
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(queryset, Weight.objects.filter(pk=self.weight.pk), transform=lambda x: x)

    def test_get_template_names(self):
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        view = VitalDetail(kwargs={'vital':self.weight.name, 'pk':self.weight.pk})
        view.request = request
        template = view.get_template_names()
        self.assertEqual(template, 'vitals/vital_detail.html')

class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_context_data(self):
        response = self.client.get(reverse('vitals:index'))
        self.assertIn('weight_list', response.context)
        """request = self.factory.get('/fake-path')
        request.user = self.user
        view = IndexView(template_name="index.html")
        context = view.get_context_data()
        self.assertEqual(context['weight'], 'weight')"""

