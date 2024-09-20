from django import forms
from django.contrib.auth.models import User

from db_models.gearstore import UserProfile, Category, Gear, AdminPassword, PageContents, CONTACT_CHOICES, BookingComments, \
    STATUS_CHOICES, Booking


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please the enter the new category info below.",
                           )
    description = forms.CharField(max_length=128)
    dateAdded = forms.DateField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', 'description', 'picture')


class GearForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please the enter the gear name.")
    deposit = forms.CharField(max_length=16)
    description = forms.CharField(max_length=128)
    dateAdded = forms.DateField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False)
    size = forms.CharField(max_length=128)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Gear
        exclude = ('category',)
        fields = ('name', 'description', 'picture', 'size', 'deposit')


class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AdminPassword
        fields = ('password',)


class PageContentsForm(forms.ModelForm):
    background_image = forms.ImageField(required=False)
    logo_image = forms.ImageField(required=False)
    home_contents = forms.CharField(widget=forms.Textarea)
    about_contents = forms.CharField(widget=forms.Textarea)
    contact_contents = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=128)
    contact_option = forms.ChoiceField(choices=CONTACT_CHOICES)
    title = forms.CharField(max_length=32)

    class Meta:
        model = PageContents
        fields = ('background_image',
                  'logo_image',
                  'home_contents',
                  'about_contents',
                  'contact_contents',
                  'contact',
                  'contact_option'
                  )


class BackgroundImageForm(forms.ModelForm):
    class Meta:
        model = PageContents
        fields = ('background_image',)


class LogoImageForm(forms.ModelForm):
    class Meta:
        model = PageContents
        fields = ('logo_image',)


class BookingCommentsForm(forms.ModelForm):
    class Meta:
        model = BookingComments
        fields = ('comment',)


class IconImageForm(forms.ModelForm):
    class Meta:
        model = PageContents
        fields = ('icon_image',)
