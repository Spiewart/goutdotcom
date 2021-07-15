import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import reverse

from goutdotcom.lab.forms import UrateForm
from goutdotcom.lab.models import Urate
from goutdotcom.lab.tests.factories import UrateFactory
from goutdotcom.lab.views import LabUpdate
from goutdotcom.users.models import User

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request

def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request 

class TestLabUpdate:
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_get_success_url(self, lab: Urate, rf: RequestFactory):
        view = LabUpdate()
        request = rf.get("/fake-url/")
        request.lab = lab

        view.request = request

        assert view.get_success_url() == f"/lab/{lab.pk}/"