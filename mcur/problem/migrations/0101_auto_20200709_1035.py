# Generated by Django 3.0.1 on 2020-07-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0100_auto_20200708_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='lvl',
            field=models.CharField(choices=[('w', 'Запись'), ('r', 'Чтение')], help_text='Уровень доступа', max_length=40, verbose_name='Уровень доступа'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('1', 'Утверждено'), ('0', 'На согласовании'), ('2', 'Ответ отклонен')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='statussys',
            field=models.CharField(choices=[('2', 'На модерации'), ('0', 'Закрыто'), ('1', 'В работе')], default='2', help_text='Статус проблемы', max_length=70, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='visible',
            field=models.CharField(choices=[('1', 'Показывать'), ('2', 'Временно скрыто'), ('0', 'Не показывать')], default='1', help_text='Режим показа на сайте', max_length=50, verbose_name='Режим'),
        ),
    ]