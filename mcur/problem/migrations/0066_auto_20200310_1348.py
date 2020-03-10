# Generated by Django 3.0.1 on 2020-03-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0065_auto_20200310_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='parsing',
            field=models.CharField(choices=[('1', 'Обновлено'), ('0', 'На обновлении')], default='0', help_text='Статус парсинга', max_length=50, verbose_name='Статус парсинга'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='visible',
            field=models.CharField(choices=[('2', 'Временно скрыто'), ('1', 'Показывать'), ('0', 'Не показывать')], default='1', help_text='Режим показа на сайте', max_length=50, verbose_name='Режим'),
        ),
        migrations.AlterField(
            model_name='term',
            name='status',
            field=models.CharField(choices=[('2', 'Исполнено'), ('1', 'На согласовании'), ('0', 'На исполнении')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
    ]
