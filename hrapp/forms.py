from django import forms
from hrapp.models import Company, Departament, Position, Worker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CompanyForm(forms.ModelForm):
    title_com = forms.CharField(max_length=50, label=(u'Название предприятия'))

    class Meta:
        model = Company
        fields = ('title_com',)


class DepartamentForm(forms.ModelForm):
    title_dep = forms.CharField(max_length=50, label=(u'Название отдела'))

    class Meta:
        model = Departament
        fields = ('title_dep',)


class PositionForm(forms.ModelForm):
    title_pos = forms.CharField(max_length=50, label=(u'Название должности'))

    class Meta:
        model = Position
        fields = ('title_pos',)


class UserForm(UserCreationForm):
    username = forms.CharField(label=(u'Введите имя пользователя'), max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=(u'Введите адрес лектронной почты'), max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=(u'Введите пароль'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=(u'Повторите пароль'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(label=(u'Имя пользователя'), max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=(u'Пароль'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
