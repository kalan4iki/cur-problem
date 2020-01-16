# Generated by Django 3.0.1 on 2020-01-13 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='curat',
        ),
        migrations.AddField(
            model_name='problem',
            name='curat',
            field=models.ManyToManyField(blank=True, help_text='Куратор', null=True, to='problem.Curator', verbose_name='Куратор'),
        ),
    ]