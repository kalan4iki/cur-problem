# Generated by Django 3.0.1 on 2020-03-10 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0062_auto_20200306_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('1', 'Утверждено'), ('0', 'На согласовании'), ('2', 'Ответ отклонен')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='parsing',
            field=models.CharField(choices=[('0', 'На обновлении'), ('1', 'Обновлено')], default='0', help_text='Статус парсинга', max_length=50, verbose_name='Статус парсинга'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='statussys',
            field=models.CharField(choices=[('1', 'В работе'), ('2', 'На модерации'), ('0', 'Закрыто')], default='2', help_text='Статус проблемы', max_length=70, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='visible',
            field=models.CharField(choices=[('0', 'Не показывать'), ('1', 'Показывать'), ('2', 'Временно скрыто')], default='1', help_text='Режим показа на сайте', max_length=50, verbose_name='Режим'),
        ),
    ]
