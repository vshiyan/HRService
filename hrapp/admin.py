from django.contrib import admin
from hrapp.models import Company, Departament, Position, Worker

# Register your models here.
admin.site.register(Company),
admin.site.register(Departament),
admin.site.register(Position),
admin.site.register(Worker)
