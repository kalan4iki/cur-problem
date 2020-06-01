# -*- coding: utf-8 -*-
#Исполняемый файл работы парсера
from django.core.management.base import BaseCommand
from problem.models import Problem, Author
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Команда запуска парсера vmeste.mosreg.ru'

    def handle(self, *args, **options):
        #pkauthor = [946,1515,155,189,540,500,561,982,198,55,157,261,130,99,82,100]
        pkauthor = [946]
        for aupk in pkauthor:
            author = Author.objects.get(pk=aupk)
            print(f'''Автор: 
            Имя: {author.fio}
            Почта: {author.email}
            Телефон: {author.tel}''')
            with open(f'export/{author.fio}.csv', 'w+') as file:
                file.writelines(f'Автор;{author.fio};{author.email};{author.tel}\n')
                all = Problem.objects.filter(author=author)
                file.writelines(f'Количество обращений за весь период;{len(all)}\n')
                file.writelines(f'Количество обращений за май;\n')
                file.writelines(f'Количество обращений за период 15.05-21.05;\n')
                file.writelines(f'Количество обращений за период 22.05-27.05;\n')
                file.writelines(f'\n')
                file.writelines(f'\n')
                temp = [1,2,3]
                for r in temp:
                    if int(r) == 1:
                        dateot = '01.05.2018'
                        datedo = '27.05.2020'
                    elif int(r) == 2:
                        dateot = '15.05.2020'
                        datedo = '21.05.2020'
                    elif int(r) == 3:
                        dateot = '22.05.2020'
                        datedo = '27.05.2020'
                    dateot2 = dateot.split('.')
                    datedo2 = datedo.split('.')
                    dates = [date(int(dateot2[2]),int(dateot2[1]),int(dateot2[0])),date(int(datedo2[2]),int(datedo2[1]),int(datedo2[0]))]
                    a = Problem.objects.filter(author=author, datecre__range=dates).order_by('datecre')
                    if a:
                        file.writelines(f'Дата отчетности;{dateot};{datedo}\n')
                        file.writelines(f'№ обращения;Дата создания;Категория\n')
                        for i in a:
                            file.writelines(f'{i.nomdobr};{i.datecre};{i.temat.name}\n')
                    file.writelines(f'Всего обращений;{len(a)}\n')
                    file.writelines(f'\n')
                    
                