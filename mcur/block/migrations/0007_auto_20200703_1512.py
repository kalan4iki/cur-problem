# Generated by Django 3.0.1 on 2020-07-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0006_auto_20200622_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='status',
            field=models.CharField(choices=[('2', 'Закрыто'), ('1', 'На блокировке'), ('0', 'В работе'), ('3', 'Отклонено'), ('4', 'На согласовании')], default='4', help_text='Статус блокировки', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='result',
            name='chstatus',
            field=models.CharField(choices=[('2', 'Закрыто'), ('1', 'На блокировке'), ('0', 'В работе'), ('3', 'Отклонено'), ('4', 'На согласовании')], default='1', help_text='Статус блокировки', max_length=50, verbose_name='Статус'),
        ),
    ]
