import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label='ФИО',
        max_length=150
    )

    email = forms.EmailField(
        label='Электронная почта'
    )

    consent = forms.BooleanField(
        label='Согласен на обработку персональных данных',
        required=True
    )

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Логин',
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.fullmatch(r'[A-Za-z0-9-]+', username):
            raise forms.ValidationError(
                'Логин должен содержать латинские буквы, цифры и дефис.'
            )

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']

        if not re.fullmatch(r'[А-Яа-яЁё -]+', full_name):
            raise forms.ValidationError(
                'ФИО должно содержать только кириллицу, пробелы и дефисы.'
            )

        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

