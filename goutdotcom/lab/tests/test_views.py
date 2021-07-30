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

