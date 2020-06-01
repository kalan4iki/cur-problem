from problem.models import Problem, Author
from datetime import datetime, date


pkauthor = int(input('Введите номер автора: '))
author = Author.objects.get(pk=pkauthor)
print(f'''Автор: 
Имя: {author.fio}
Почта: {author.email}
Телефон: {author.tel}''')
print('Формат даты: день.месяц.год')
dateot = input('Введите дату отсчета: ')
datedo = input('Введите дату окончания: ')
dateot2 = dateot.split('.')
datedo2 = datedo.split('.')
dates = [date(int(dateot2[2]),int(dateot2[1]),int(dateot2[0])),date(int(datedo2[2]),int(datedo2[1]),int(datedo2[0]))]
a = Problem.objects.filter(author=author, datecre__range=dates)
if a:
    with open(f'export/{author.fio}-{dateot}-{datedo}.txt', 'w') as file:
        for i in a:
            file.writelines(f'№{i.nomdobr}. Дата создания{i.datecre}. Категория: {i.temat.name}. ')