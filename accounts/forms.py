from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords Dont Match')
        return cd['password2']
    
    def save(self, commit = True):
        user =  super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\">this link</a>')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegisterationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    full_name = forms.CharField(max_length=200, label='Full Name')
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(max_value=99999, min_value=10000)