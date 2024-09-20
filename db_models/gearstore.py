import string
from datetime import timedelta
from io import BytesIO

import django
import qrcode
from django.apps import AppConfig
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
import random

WHATSAPP = 'logo-whatsapp'
PHONE = 'call-outline'
EMAIL = 'mail-outline'

CONTACT_CHOICES = (
    (WHATSAPP, 'WhatsApp'),
    (PHONE, 'Phone Number'),
    (EMAIL, 'Email'),
)

PRIMARY_PURPOSE = "Affiliated"
SECONDARY_PURPOSE = "Personal"

PURPOSE_CHOICES = (
    (PRIMARY_PURPOSE, PRIMARY_PURPOSE),
    (SECONDARY_PURPOSE, SECONDARY_PURPOSE),
)

ACTIVE = 'Active'
REQUESTED = 'Requested'
ACCEPTED = 'Accepted'
DENIED = 'Denied'
RETURNED = 'Returned'
NOT_RETURNED = 'Unreturned'

STATUS_CHOICES = (
    (ACTIVE, ACTIVE),
    (REQUESTED, REQUESTED),
    (ACCEPTED, ACCEPTED),
    (DENIED, DENIED),
    (RETURNED, RETURNED),
    (NOT_RETURNED, NOT_RETURNED),
)

IN_SERVICE = 'In Service'
OUT_OF_SERVICE = 'Out Of Service'

GEAR_STATUS_CHOICES = (
    (IN_SERVICE, 'In Service'),
    (OUT_OF_SERVICE, 'Out Of Service'),
)


# define a method to generate a random id not in use for bookings
def id_generator():
    ID_LENGTH = 6
    # define a string to hold the id
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=ID_LENGTH))
    try:
        booking = Booking.objects.get(id=id)
        print("Booking ID already exists. Creating new ID.")
        return id_generator()
    except Booking.DoesNotExist:
        print("Booking ID is valid.")
        return id


# define a method to generate a random id not in use for comments
def comment_id_generator():
    ID_LENGTH = 6
    # define a string to hold the id
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=ID_LENGTH))
    try:
        booking = BookingComments.objects.get(id=id)
        print("Booking ID already exists. Creating new ID.")
        return id_generator()
    except BookingComments.DoesNotExist:
        print("Booking ID is valid.")
        return id


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to="gearstore/category_images", default="gearstore/category_images/default.png")
    slug = models.SlugField(unique=True, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        app_label = 'gearstore_app'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adminStatus = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, default="Jane")
    last_name = models.CharField(max_length=30, default="Doe")
    picture = models.ImageField(upload_to='gearstore/profile_images', default="gearstore/profile_images/default.jpeg")

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'gearstore_app'


class Gear(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    deposit = models.TextField(max_length=16, default="Free")
    description = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=GEAR_STATUS_CHOICES, default=IN_SERVICE)
    dateAdded = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to="gearstore/gear_images", default="gearstore/gear_images/default.png")
    size = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = "Gear"
        app_label = 'gearstore_app'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Gear, self).save(*args, **kwargs)

    def is_available(self):
        bookings = Booking.objects.all().filter(gearItem=self)
        for booking in bookings:
            if booking.dateBorrowed <= timezone.now().date() and booking.dateToReturn >= timezone.now().date():
                if not (booking.status == "Returned" or booking.status == "Denied"):
                    return False, booking
        return True, None


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)


class Booking(models.Model):
    id = models.TextField(max_length=6, primary_key=True, default=id_generator)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    purpose = models.TextField(choices=PURPOSE_CHOICES, default=SECONDARY_PURPOSE)
    gearItem = models.ForeignKey(Gear, on_delete=models.CASCADE)
    dateBorrowed = models.DateField(auto_now_add=True)
    dateToReturn = models.DateField(default=return_date_time)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=REQUESTED)

    def __str__(self):
        return f"{self.user.user.username} booking of {self.gearItem.name}"

    def is_current(self):
        if self.dateToReturn >= timezone.now().date():
            return True
        return False

    class Meta:
        app_label = 'gearstore_app'


class QR_Code(models.Model):
    qr_code = models.ImageField(upload_to="gearstore/qrcode_images", default="gearstore/qrcode_images/default_qrcode.png")
    domain = models.TextField(default="")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, primary_key=True)

    def update_qrcode(self):
        content = PageContents.objects.all()
        if content:
            content = content[0]
            if content.domain != self.domain:
                self.domain = content.domain

                img = qrcode.make(self.domain + '/gear-store/booking/' + self.booking.id)
                stream = BytesIO()
                img.save(stream, 'png')
                img_url = 'qrcode_' + self.booking.id + '.png'
                self.qr_code.save(img_url, File(stream), save=False)
                self.save()

    class Meta:
        app_label = 'gearstore_app'


class AdminPassword(models.Model):
    id = models.TextField(max_length=6, primary_key=True, default=id_generator)
    password = models.CharField(max_length=64, default="password123")

    def __str__(self):
        return self.password

    class Meta:
        app_label = 'gearstore_app'


class PageContents(models.Model):
    background_image = models.ImageField(upload_to="gearstore/site_images", default="gearstore/site_images/default_background.jpg")
    logo_image = models.ImageField(upload_to="gearstore/site_images", default="gearstore/site_images/default_logo.png")
    icon_image = models.ImageField(upload_to="gearstore/site_images", default="gearstore/site_images/default_icon.png", )
    home_contents = models.TextField(default="")
    about_contents = models.TextField(default="")
    contact_contents = models.TextField(default="")
    contact = models.CharField(max_length=128, default="07123 456 789")
    contact_option = models.CharField(max_length=128, choices=CONTACT_CHOICES, default=PHONE)
    title = models.TextField(default="Gear Store")
    domain = models.URLField(default="")
    auto_increment_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'gearstore_app'


class BookingComments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    comment = models.TextField()
    starred = models.BooleanField(default=False)
    id = models.TextField(max_length=6, primary_key=True, default=comment_id_generator)
    dateAdded = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'gearstore_app'


class SidebarLinks(models.Model):
    link_text = models.TextField()
    url = models.URLField()
    id = models.TextField(max_length=6, primary_key=True, default=comment_id_generator)

    class Meta:
        app_label = 'gearstore_app'
