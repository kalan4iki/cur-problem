# Generated by Django 3.0.1 on 2020-07-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0048_auto_20200708_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionhistory',
            name='status',
            field=models.CharField(choices=[('1', 'Выполнено'), ('0', 'На выполнении'), ('2', 'Ошибка')], default='0', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='loggings',
            name='name',
            field=models.CharField(choices=[('0', 'Добавлено'), ('2', 'Прочее'), ('1', 'Обновлено')], default='0', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='logspars',
            name='name',
            field=models.CharField(choices=[('1', 'Изменение подкатегории'), ('3', 'Обновление даты ответа'), ('0', 'Изменение тематики'), ('4', 'Обновление статуса'), ('2', 'Добавление автора')], default='0', max_length=255, null=True, verbose_name='Название операции'),
        ),
    ]
