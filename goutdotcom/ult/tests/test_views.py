from django.apps import apps
from django.test import RequestFactory, TestCase
from django.urls import reverse

from goutdotcom.users.tests.factories import UserFactory

from ..views import ULTCreate, ULTDetail, ULTUpdate

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

    def test_get_404(self):
        request = self.factory.get(self.detail_url)
        request.user = self.user2
        ### response with fake Weight object's name, pk for VitalDetail view
        view = VitalDetail.as_view()
        response = view(request, user=self.user, vital=self.weight.name, pk=self.weight.pk)
        self.assertEqual(response.status_code, 404)

    def test_get_template_names(self):
        request = self.factory.get(self.detail_url)
        request.user = self.user
        ### response with fake Weight object's name, pk for VitalDetail view
        view = VitalDetail(kwargs={'vital':self.weight.name, 'pk':self.weight.pk})
        view.request = request
        template = view.get_template_names()
        self.assertEqual(template, 'vitals/vital_detail.html')
