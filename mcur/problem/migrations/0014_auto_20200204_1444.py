# Generated by Django 3.0.1 on 2020-02-04 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0013_auto_20200204_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['pk'], 'verbose_name': 'ответ', 'verbose_name_plural': 'ответы'},
        ),
        migrations.AddField(
            model_name='term',
            name='otv',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.Answer'),
        ),
        migrations.AlterField(
            model_name='access',
            name='lvl',
            field=models.CharField(choices=[('w', 'Запись'), ('r', 'Чтение')], help_text='Уровень доступа', max_length=40, verbose_name='Уровень доступа'),
        ),
        migrations.AlterField(
            model_name='term',
            name='status',
            field=models.CharField(choices=[('1', 'На согласовании'), ('2', 'Исполнено'), ('0', 'На исполнении')], default='0', help_text='Статус ответа', max_length=50, verbose_name='Статус'),
        ),
    ]
