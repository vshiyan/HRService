# Generated by Django 2.1 on 2018-08-09 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrapp', '0004_auto_20180809_0602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='title',
            new_name='title_com',
        ),
        migrations.RenameField(
            model_name='departament',
            old_name='title',
            new_name='title_dep',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='title',
            new_name='title_pos',
        ),
    ]
