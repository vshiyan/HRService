from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Company(models.Model):
    """Model describes company"""
    title_com = models.CharField(max_length=100, verbose_name='Название компании')

    def __str__(self):
        return self.title_com


class Departament(models.Model):
    """Model describes deportament"""
    title_dep = models.CharField(max_length=100, verbose_name='Название отдела')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Название компании')

    def __str__(self):
        return self.title_dep


class Position(models.Model):
    """Model describes position"""
    title_pos = models.CharField(max_length=100, verbose_name='Название должности')
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, verbose_name='Название отдела')
    vakant = models.BooleanField()

    def __str__(self):
        return self.title_pos


class Worker(models.Model):
    """Model describes user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CHOICES_ROLE = (
        ('admin', 'Главный администратор компании'),
        ('worker', 'Наемный рабочий'),
        ('hrworker', 'Работник отдела кадров')
    )
    role = models.CharField(max_length=10, choices=CHOICES_ROLE, verbose_name='Роль работника')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Название должности')
    vakant = models.BooleanField()
    about = models.CharField(max_length=1200, verbose_name='О себе', blank=True)
    education = models.CharField(max_length=400, blank=True, verbose_name='Образование')

    def __str__(self):
        return self.user.username

    def lay_off(self):
        position = Position.objects.get(pk=self.position.pk)
        position.vakant = True
        position.save()
        self.vakant = True
        self.position = None
        self.save()
