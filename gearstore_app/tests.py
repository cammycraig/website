from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve
from .forms import SignupForm, LoginForm