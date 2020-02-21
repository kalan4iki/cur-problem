from django.db import models

# Create your models here.
class Parser(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 40, help_text = 'Название парсера',
                            verbose_name = 'Парсер')
    datecre = models.DateField(auto_now_add=True, help_text='Дата создания', verbose_name = 'Дата создания', blank=True, null=True)
    status = models.CharField(max_length=70, help_text='Статус проблемы',
                            verbose_name = 'Статус', default='2',choices=stat)


    class Meta:
        ordering = ['datecre']
        verbose_name = 'парсер'
        verbose_name_plural = 'парсеры'

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse("problem", args=(self.nomdobr,)) # TODO: Добавить url
