from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
import pytz
from timezone_field import TimeZoneField