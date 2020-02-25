# Generated by Django 3.0.1 on 2020-02-25 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0052_auto_20200225_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='problem.Curator', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('2', 'Ответ отклонен'), ('1', 'Утверждено'), ('0', 'На согласовании')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='parsing',
            field=models.CharField(choices=[('0', 'На обновлении'), ('1', 'Обновлено')], default='0', help_text='Статус парсинга', max_length=50, verbose_name='Статус парсинга'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='statussys',
            field=models.CharField(choices=[('0', 'Закрыто'), ('1', 'В работе'), ('2', 'На модерации')], default='2', help_text='Статус проблемы', max_length=70, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='visible',
            field=models.CharField(choices=[('0', 'Не показывать'), ('1', 'Показывать')], default='1', help_text='Режим показа на сайте', max_length=50, verbose_name='Режим'),
        ),
        migrations.AlterField(
            model_name='termhistory',
            name='curatuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='curatuserterm', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
    ]
