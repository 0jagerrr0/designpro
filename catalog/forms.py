import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .models import DesignRequest, Category


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.errors:
            self.fields[field_name].widget.attrs['class'] = 'input-error'

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

        if not re.fullmatch(r'[A-Za-z-]+', username):
            raise forms.ValidationError(
                'Логин должен содержать только латинские буквы и дефис.'
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


class RequestForm(forms.ModelForm):
    room_image = forms.ImageField(
        label='Фото помещения или план',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']
            )
        ]
    )

    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'room_image']
        labels = {
            'title': 'Название заявки',
            'description': 'Описание',
            'category': 'Категория',
        }

    def clean_room_image(self):
        image = self.cleaned_data['room_image']

        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                'Размер изображения не должен превышать 2 МБ.'
            )

        return image


class AcceptRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['admin_comment']
        labels = {
            'admin_comment': 'Комментарий администратора',
        }

    def clean_admin_comment(self):
        comment = self.cleaned_data['admin_comment'].strip()

        if not comment:
            raise forms.ValidationError(
                'Необходимо указать комментарий.'
            )

        return comment


class CompleteRequestForm(forms.ModelForm):
    design_image = forms.ImageField(
        label='Изображение готового дизайна'
    )

    class Meta:
        model = DesignRequest
        fields = ['design_image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории',
        }
