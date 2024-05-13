from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.files.images import get_image_dimensions

CustomUser = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'autocomplete': 'email'
    }))
    firstname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'autocomplete': 'given-name',
        'required': False
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'autocomplete': 'family-name',
        'required': False
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'autocomplete': 'new-password'
    }))
    picture = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'help_text': 'Optional. '
                     'You can upload a profile picture later.'
    }), required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'firstname',
                  'surname', 'password1', 'password2', 'picture']

    def clean_picture(self):
        picture = self.cleaned_data.get('picture', None)
        if picture:
            try:
                w, h = get_image_dimensions(picture)
                max_width = max_height = 1024
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        (f'Please use an image that is {max_width} x {max_height}'
                         f'pixels or smaller.'))
                main, sub = picture.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'png', 'jpg']):
                    raise forms.ValidationError('Please use a JPEG or PNG image.')
                if picture.size > (20 * 1024 * 1024):
                    raise forms.ValidationError('Avatar file size may not exceed 20mb.')
            except (AttributeError, TypeError):
                pass
        return picture

    def save(self, commit=True):
        user = super().save(commit=False)
        user.firstname = self.cleaned_data['firstname']
        user.surname = self.cleaned_data['surname']
        if self.cleaned_data['picture']:
            user.picture = self.cleaned_data['picture']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            'firstname', 'surname', 'timezone',
            'bio', 'picture'
        ]
        widgets = {
            'firstname' : forms.TextInput(),
            'surname' : forms.TextInput(),
            #Values is many to many so requires the ability to select
            #more than one value
            #SelectMultiple found at:
            #https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
            'timezone': forms.Select(attrs={'class': 'base.css'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'picture': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, (forms.CharField,
                                            forms.ChoiceField, forms.FileField)):
                field.required = False
