from fractions import Fraction
from typing import NoReturn
import numpy as np

print('\nРешение задачи линейного программирования симплекс-методом\n')
print('''Данная программа решает ЗЛП симплекс-методом. На момент ввода данных задача должна быть приведена к каноническому виду!
Необходимо заменить неравенства в ограничениях на равенства, добавив новые переменные, коэффициент которых должен быть строго равен 1,
не -1! Например, если разных переменных всего 5, то нужно указать коэффициенты всех 5 переменных в каждом уравнении, причем количество переменных
в системе ограничений и в целевой функции должно быть одинаково. При отсутствии переменной в одном из уравнений приравнять ее коэффициент к нулю
Б - базис; Кб - коэффициенты базиса; А1, А2, ... Аn - векторы; А0 - вектор свободных членов\n''')

## Инициализация переменных ##

# Инициализация коэффициентов целевой функции
while True:
    try:
        main_function = list(map(int, input('Введите коэффициенты целевой функции Z(X) через пробел (Z(X) = x1 + x3 - 7 –> "1 0 2 -7"):\n').split()))
    except:
        print('Ошибка ввода\n')
    else:
        break

# Инициализация направления целевой функции (к минимуму или к максимуму)
while True:
    target = input('Функция стремится к максимуму или к минимуму? (введите max или min):\n')
    if target not in ('min', 'max'):
        print('Неправильное значение. Введите min или max\n')
    else:
        break

# Ввод количества ограничений-уравнений
while True:
    try:
        n = int(input('Введите количество ограничений-уравнений:\n'))
    except:
        print('Нужно ввести одно единственное число!\n')
    else:
        break

#Формирование системы из уравнений-ограничений
while True:
    print('Вводите ограничения в формате "1 0 -4 19" (x1 -4*x3 = 19)\nВвод:  ')
    restrictions = [list(map(int, input().split())) for _ in range(n)]
    if min(map(len, restrictions)) == max(map(len, restrictions)) and all(map(lambda x: len(x) >= 2, restrictions)): #проверка равенства длин уравнений и условия, что каждое >=2
        if any(map(lambda x: len(x) != len(main_function), restrictions)): #проверка равенства длины уравнений с длиной целевой функцией
            print('Целевая функция и ограничения имеют разное число коэффициентов!\n')
            continue
        break
    else:
        print('Число коэффициентов должно быть одинаковым и не менее 2!\n')


## Блок создания функций ##

# Функция для вывода целевой функции
def print_main_function(main_function: list[int], target: str) -> NoReturn:
    '''Функция выводит целевую функцию на экран, принимая в качестве
    аргумента список ее коэффициентов'''
    show_main_function = ''
    for ind, coef in enumerate(main_function[:-1], 1):
        if coef == 0:
            continue
        elif coef > 0:
            if coef == 1:
                coef = ''
            else:
                coef = str(coef) + '*'
            show_main_function += f' + {coef}x{ind}'
        else:
            if coef == -1:
                coef = ''
            else:
                coef = str(abs(coef)) + '*'
            show_main_function += f' - {coef}x{ind}'
    if main_function[-1] > 0:
        show_main_function += ' + ' + str(main_function[-1])
    elif main_function[-1] < 0:
        show_main_function += ' - ' + str(abs(main_function[-1]))
    if show_main_function[1] == '+':
        show_main_function = show_main_function[3:]
    else:
        show_main_function = '-' + show_main_function[3:]
    print(f'\nZ(X) = {show_main_function} –> {target}\n')

# Функция для вывода уравнения пользователю
def print_equations(equations: list[list[int]]) -> NoReturn:
    '''Функция выводит уравнения с заданными коэффициентами. Перебор всех
    коэффициентов происходит через цикл for, кроме последнего,
    так как он будет добавлен в конце со знаком "=". Для красоты
    1 и -1 меняются на + и - без коэффициентов, причем + опускается
    полностью, если стоит в начале.'''
    for equation in equations:
        string_equation = ''
        for ind, coef in enumerate(equation[:-1], 1):
            if coef == 0:
                continue
            elif coef > 0:
                if coef == 1:
                    coef = ''
                else:
                    coef = str(coef) + '*'
                string_equation += f' + {coef}x{ind}'
            else:
                if coef == -1:
                    coef = ''
                else:
                    coef = str(abs(coef)) + '*'
                string_equation += f' - {coef}x{ind}'
        string_equation += f' = {equation[-1]}'
        if string_equation[1] == '+':
            string_equation = string_equation[3:]
        else:
            string_equation = '-' + string_equation[3:]
        print(string_equation)

# Функция для транспонирования матрицы
def form_vectors(equations: list[list[int]]) -> list[list[int]]:
    '''Функция возвращает транспонированную матрицу, упрощая работу с векторами.
    Часто будет использована внутри других функций'''
    arr = np.array(equations)
    transposed_arr = np.transpose(arr)
    transposed_equations = [list(el) for el in transposed_arr]
    return transposed_equations

# Функция для поиска индекса векторов, входящих в базис
def find_basis(equations: list[list[int]]) -> list[int]:
    '''Функция возвращает список индексов векторов, входящих в базис'''
    basis = []
    x = form_vectors(equations)
    for i, el in enumerate(x):
        if set(el) == {0, 1}:
            basis.append((el, i))
    return [el[1] for el in sorted(basis, key=lambda x: x[0], reverse=True)]

# Функция для поиска коэффициентов базисных векторов из целевой функции
def find_basis_coefs(indexes_of_basis: list[int]) -> list[int]:
    return list(map(lambda i: main_function[i], indexes_of_basis))

# Функция для поиска оценок векторов
def find_estimates(coefs: list[int], equations: list[list[int]]) -> list[int]:
    '''Функция возвращает список оценок, основываясь на коэффициентах базиса
    и на матрице уравнений'''
    vectors, estimates = form_vectors(equations), []
    for i, vector in enumerate(vectors):
        product = map(lambda x, y: x*y, vector, coefs)
        if i == len(vectors) - 1:
            estimates.append(sum(product) + main_function[i])
        else:
            estimates.append(sum(product) - main_function[i])
    return estimates

# Вывод промежуточных результатов
def print_results(equations: list[list[int]], estimates: list[int], basis_coefs: list[int], basis_indexes: list[int]) -> NoReturn:
    '''Функция ничего не возвращает, выводит промежуточные результаты работы с матрицами'''
    upper_row = ['Б', 'Кб'] + [f'A{i}' for i in range(1, len(main_function))] + ['A0']
    max_indent = max(3, max([max(map(len, [str(y) for y in bebra])) for bebra in equations]))
    string_upper_row = '  '.join([el.ljust(max_indent) for el in upper_row])
    print(string_upper_row)
    for i in range(len(equations)):
        list_row = [f'A{basis_indexes[i] + 1}', str(basis_coefs[i]), *[str(el) for el in equations[i]]]
        string_row = [el.ljust(max_indent) for el in list_row]
        print('  '.join(string_row))
    string_estimates = '  '.join([x.ljust(max_indent) for x in [str(el) for el in estimates]])
    print('Оценки:'.ljust(len('  '.join(string_row[:2]) + ' ')), string_estimates)

# Проверка условий
def is_problem(target: str, estimates: list[int]) -> bool:
    return (target == 'max' and all(map(lambda x: x >= 0, estimates[:-1]))) or (target == 'min' and all(map(lambda x: x <= 0, estimates[:-1])))

# Поиск индексов векторов, чьи оценки не соответствуют условиям
def find_inds_of_problems(estimates: list[int]) -> list[int]:
    '''Функция возвращает список индексов векторов, чьи оценки не соответствуют условиям,
    принимая в качестве аргумента список оценок'''
    inds_of_problems = []
    for i in range(len(main_function) - 1):
        if (target == 'max' and estimates[i] < 0) or (target == 'min' and estimates[i] > 0):
            inds_of_problems.append(i)
    return inds_of_problems

# Функция для поиска параметров-тета
def find_tetas(estimates: list[int], equations: list[list[int]]) -> list[list[int]]:
    '''Функция возвращает список, внутри которого находятся списки, характеризующие
    параметры тета, которые находятся для определения опорного элемента'''
    inds_of_problems, vectors, tetas = find_inds_of_problems(estimates), form_vectors(equations), []
    for i in inds_of_problems:
        teta = []
        for k in range(len(vectors[i])):
            try:
                if equations[k][-1] % vectors[i][k] != 0:
                    x = Fraction(equations[k][-1], vectors[i][k])
                else:
                    x = equations[k][-1] // vectors[i][k]
                if x <= 0: # Фильтрует неположительные значения координат тета
                    teta.append('-')
                else:
                    teta.append(x)
            except: # Исключает ситуацию деления координаты вектора А0 на нулевую координату Аj
                teta.append('-')
        tetas.append(teta)
    return tetas

# Поиск координат точки, которую надо взять за единицу в системе векторов на основе параметров-тета и оценок
def find_the_coordinates(tetas: list[list[int]], estimates: list[int]) -> tuple[int]:
    '''Функция возвращает кортеж вида (i, j) из координат опорного элемента, который необходимо представить единицей'''
    least_tetas = []
    for i in range(len(tetas)):
        x = []
        for k in range(len(tetas[i])): # фильтрация '-'
            if type(tetas[i][k]) != str:
                x.append((tetas[i][k], k))
        least_tetas.append(min(x, key=lambda x: x[0]))
    indexes = enumerate(find_inds_of_problems(estimates))
    res = [(-least_tetas[i_teta][0] * estimates[i_est], (least_tetas[i_teta][1], i_est)) for i_teta, i_est in indexes]
    if target == 'max':
        return max(res, key=lambda x: x[0])[1]
    else:
        return min(res, key=lambda x: x[0])[1]
        
# Вывод параметров-тета и комментариев по поводу опорного элемента
def print_tetas(tetas: list[list[int]], estimates: list[int]) -> NoReturn:
    '''Функция выводит параметры тета и координаты опорного элемента'''
    inds_of_problems = find_inds_of_problems(estimates)
    string_tetas = [[str(x) for x in el] for el in tetas]
    string_res = 'Тета: ', {f'θ{i + 1}': t for t, i in zip(string_tetas, inds_of_problems)}
    print(*string_res)

# Функция вывода координат
def print_coordinates(support_el_coords: tuple[int]) -> NoReturn:
    row, col = (1 + el for el in support_el_coords)
    print(f'Опорным является элемент по координатам: строка = {row}, столбец = {col}')

# Функция преобразований Жордана-Гаусса
def jordan_gaus(equations: list[list[int]], support_el_coords: tuple[int]) -> NoReturn:
    '''Функция ничего не возвращает. Она преобразовывает матрицу уравнений, по отношению к опорному элементу
    по координатам в кортеже support_el_coords'''
    i, j = support_el_coords
    denom = equations[i][j]
    def division(arr: list[int], denom: int):
        '''Функция получает список и делитель, а возвращает список, где каждый элемент поделен'''
        new_arr = []
        for el in arr:
            if type(el) == int: # если элемент целый
                if el % denom == 0: # если целочисленное деление получается
                    new_arr.append(el // denom)
                else: # иначе превращаем в дробь
                    new_arr.append(Fraction(el, denom))
            else: # если элемент уже дробный
                new_arr.append(el / denom)
        return new_arr
    equations[i] = division(equations[i], denom) # изменяем строку с опорным элементом на полученный список
    rows_to_change = sorted(set(range(len(equations))).difference([i]))
    for ind in rows_to_change:
        multiplier = equations[ind][j] # то на что мы будем умножать опорную строку
        for k in range(len(equations[i])): # замена координат
            equations[ind][k] = equations[ind][k] - multiplier * equations[i][k]

# Функция для вывода значений переменных Xn в ответе
def answer_xs(equations: list[list[int]]) -> str:
    s = []
    for ind, ans in zip(find_basis(equations), form_vectors(equations)[-1]):
        if main_function[ind] != 0:
            s.append(f'x{ind + 1} = {ans}')
    return ' '.join(sorted(s))

def main():
    print('Проверка введенных данных:')
    print_main_function(main_function, target)
    print_equations(restrictions)
    input('Если все нормально, введите любой символ, иначе запустите программу заново\n')
    while True:
        indexes_of_bases = find_basis(restrictions) # Поиск индексов базисных векторов
        basis_coefs = find_basis_coefs(indexes_of_bases) # Поиск коэффициентов базисных векторов из целевой функции
        estimates = find_estimates(basis_coefs, restrictions) # Поиск оценок векторов
        print_results(restrictions, estimates, basis_coefs, indexes_of_bases) # Вывод промежуточных результатов
        if is_problem(target, estimates): # Если оценки удовлетворяют условию, то ответ готов
            print(f'\nОтвет: Z(X) = {estimates[-1]} –> {target} при {answer_xs(restrictions)}')
            for i in range(len(estimates)): # Если оценка вектора, не входящего в базис, равна нулю, то задача имеет множество решений
                if estimates[i] == 0 and set(form_vectors(restrictions)[i]) != {0, 1}:
                    print('Уравнение имеет множество решений')
            break
        tetas = find_tetas(estimates, restrictions) #Находим параметры-тета для определения вектора, который нужно поместить в базис
        print_tetas(tetas, estimates) # Вывод параметров тета
        if all([all(map(lambda x: type(x) == str,el)) for el in tetas]): # Если нет параметров-тета, удовлетворяющих условию, то решений нет
            print('Нет решений')
            break
        else:
            sup_el_coords = find_the_coordinates(tetas, estimates)
            print_coordinates(sup_el_coords)
            print('-----------------------------------------------')
            jordan_gaus(restrictions, sup_el_coords) # Осуществление преобразования Жордана-Гаусса

main()
