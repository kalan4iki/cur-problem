# Generated by Django 3.0.1 on 2020-02-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0011_auto_20200204_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='lvl',
            field=models.CharField(choices=[('w', 'Запись'), ('r', 'Чтение')], help_text='Уровень доступа', max_length=40, verbose_name='Уровень доступа'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='datebzm',
            field=models.DateField(auto_now=True, help_text='Дата изменения', null=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='datecre',
            field=models.DateField(auto_now_add=True, help_text='Дата создания', null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('0', 'На согласовании'), ('1', 'Утверждено')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
    ]