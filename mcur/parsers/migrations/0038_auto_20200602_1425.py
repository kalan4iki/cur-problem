# Generated by Django 3.0.1 on 2020-06-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0037_auto_20200602_1424'),
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
            field=models.CharField(choices=[('1', 'Обновлено'), ('2', 'Прочее'), ('0', 'Добавлено')], default='0', max_length=50, verbose_name='Статус'),
        ),
    ]