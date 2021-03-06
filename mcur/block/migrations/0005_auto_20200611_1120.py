# Generated by Django 3.0.1 on 2020-06-11 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0004_auto_20200610_1000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['datecre'], 'verbose_name': 'сообщение', 'verbose_name_plural': 'сообщения'},
        ),
        migrations.AlterField(
            model_name='appeal',
            name='status',
            field=models.CharField(choices=[('1', 'На блокировке'), ('0', 'В работе'), ('3', 'Отказано'), ('2', 'Заблокировано')], default='0', help_text='Статус блокировки', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='result',
            name='chstatus',
            field=models.CharField(choices=[('1', 'На блокировке'), ('0', 'В работе'), ('3', 'Отказано'), ('2', 'Заблокировано')], default='1', help_text='Статус блокировки', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='result',
            name='nomkom',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Номер комиссии'),
        ),
    ]
