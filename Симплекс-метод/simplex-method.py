from fractions import Fraction

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

# Функция для вывода уравнения пользователю
def print_equations(equations): 
    for equation in equations:
        s = ''
        for ind, coef in enumerate(equation[:-1], 1):
            if coef == 0:
                continue
            elif coef > 0:
                if coef == 1:
                    coef = ''
                else:
                    coef = str(coef) + '*'
                s += f' + {coef}x{ind}'
            else:
                if coef == -1:
                    coef = ''
                else:
                    coef = str(abs(coef)) + '*'
                s += f' - {coef}x{ind}'
        s += f' = {equation[-1]}'
        if s[1] == '+':
            s = s[3:]
        else:
            s = '-' + s[3:]
        print(s)

# Функция для транспонирования матрицы
def form_vectors(equations):
    basis = []
    for i in range(len(equations[0])):
        vector = []
        for j in range(len(equations)):
            vector.append(equations[j][i])
        basis.append(vector)
    return basis

# Функция для поиска индекса векторов, входящих в базис
def find_basis(equations):
    basis = []
    x = form_vectors(equations)
    for i, el in enumerate(x):
        if set(el) == {0, 1}:
            basis.append((el, i))
    return [el[1] for el in sorted(basis, key=lambda x: x[0], reverse=True)]

# Функция для поиска оценок векторов
def find_estimates(coefs, equations):
    estimates = []
    for i in range(len(equations[0])):
        operated_sum = 0
        for j in range(len(equations)):
            operated_sum += equations[j][i] * coefs[j]
        if i == len(equations[0]) - 1:
            estimates.append(operated_sum + main_function[i])
        else:
            estimates.append(operated_sum - main_function[i])
    return estimates

# Вывод промежуточных результатов
def print_results(equations, estimates, coefs, basis):
    print('  '.join([el.ljust(max(3, max([max(map(len, [str(y) for y in bebra])) for bebra in equations]))) for el in (['Б', 'Кб'] + [f'A{i}' for i in range(1, len(main_function))] + ['A0'])]))
    for i in range(len(equations)):
        abc = [el.ljust(max(3, max([max(map(len, [str(y) for y in bebra])) for bebra in equations]))) for el in [f'A{basis[i] + 1}', str(coefs[i]), *[str(el) for el in equations[i]]]]
        print('  '.join(abc))
    print('Оценки:'.ljust(len('  '.join(abc[:2]) + ' ')), '  '.join([x.ljust(max(3, max([max(map(len, [str(y) for y in bebra])) for bebra in equations]))) for x in [str(el) for el in estimates]]))

# Поиск индексов векторов, чьи оценки не соответствуют условиям
def find_inds_of_problems(estimates):
    inds_of_problems = []
    for i in range(len(main_function) - 1):
        if (target == 'max' and estimates[i] < 0) or (target == 'min' and estimates[i] > 0):
            inds_of_problems.append(i)
    return inds_of_problems
# Функция для поиска параметров-тета
def find_tetas(estimates, equations):
    inds_of_problems, vectors, tetas = find_inds_of_problems(estimates), form_vectors(equations), []
    for i in inds_of_problems:
        teta = []
        for k in range(len(vectors[i])):
            try:
                if equations[k][-1] % vectors[i][k] != 0:
                    x = Fraction(equations[k][-1], vectors[i][k])
                else:
                    x = equations[k][-1] // vectors[i][k]
                if x <= 0:
                    teta.append('-')
                else:    
                    teta.append(x)
            except:
                teta.append('-')
        tetas.append(teta)
    return tetas
# Поиск координат точки, которую надо взять за единицу в системе векторов на основе параметров-тета и оценок
def find_the_coordinates(tetas, estimates):
    least_tetas = []
    for i in range(len(tetas)):
        x = []
        for k in range(len(tetas[i])):
            if type(tetas[i][k]) != str:
                x.append((tetas[i][k], k))
        least_tetas.append(min(x, key=lambda x: x[0]))
    res = [(-least_tetas[ind_tetas][0] * estimates[ind_estimates], (least_tetas[ind_tetas][1], ind_estimates)) for ind_tetas, ind_estimates in enumerate(find_inds_of_problems(estimates))]
    if target == 'max':
        return max(res, key=lambda x: x[0])[1]
    else:
        return min(res, key=lambda x: x[0])[1]
# Функция преобразований Жордана-Гаусса
def jordan_gaus(equations, coordinates):
    i, j = coordinates
    denom = equations[i][j]
    def division(arr, denom):
        new_arr = []
        for el in arr:
            if type(el) == int:
                if el % denom == 0:
                    new_arr.append(el // denom)
                else:
                    new_arr.append(Fraction(el, denom))
            else:
                new_arr.append(el / denom)
        return new_arr
    equations[i] = division(equations[i], denom)
    for ind in set(range(len(equations))).difference([i]):
        multiplier = equations[ind][j]
        for k in range(len(equations[i])):
            equations[ind][k] = equations[ind][k] - multiplier * equations[i][k]
# Функция для вывода значений переменных Xn в ответе           
def answer_xs(equations):
    s = []
    for ind, ans in zip(find_basis(equations), form_vectors(equations)[-1]):
        if main_function[ind] != 0:
            s.append(f'x{ind + 1} = {ans}')
    return ' '.join(sorted(s))

## Блок проверки данных ## (Вывод ранее введенных пользователем данных в удобочитаемом формате)
print('Проверка введенных данных:')
# Вывод целевой функции
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

print_equations(restrictions)
input('Если все нормально, введите любой символ, иначе запустите программу заново\n')

## Порядок работы программы ##
while True:
    coefs_of_basis = list(map(lambda k: main_function[k], find_basis(restrictions))) # Находим коэффициенты базисов для расчета оценок
    estimates = find_estimates(coefs_of_basis, restrictions) # Находим оценки
    print_results(restrictions, estimates, coefs_of_basis, find_basis(restrictions))
    if (target == 'max' and all(map(lambda x: x >= 0, estimates[:-1]))) or (target == 'min' and all(map(lambda x: x <= 0, estimates[:-1]))): # Если оценки удовлетворяют условию, то ответ готов
        print(f'\nОтвет: Z(X) = {estimates[-1]} –> {target} при {answer_xs(restrictions)}')
        for i in range(len(estimates)): # Если оценка вектора, не входящего в базис, равна нулю, то задача имеет множество решений
            if estimates[i] == 0 and set(form_vectors(restrictions)[i]) != {0, 1}:
                print('Уравнение имеет множество решений')
        break
    tetas = find_tetas(estimates, restrictions) #Находим параметры-тета для определения вектора, который нужно поместить в базис
    print('Тета: ', {f'θ{i + 1}': t for t, i in zip([[str(x) for x in el] for el in tetas], find_inds_of_problems(estimates))})
    if all([all(map(lambda x: type(x) == str,el)) for el in tetas]): # Если нет параметров-тета, удовлетворяющих условию, то решений нет 
        print('Нет решений')
        break
    print('-----------------------------------------------')
    coords = find_the_coordinates(tetas, estimates) # Находим точку, которую положим за 1
    jordan_gaus(restrictions, coords) # Осуществление преобразования Жордана-Гаусса
    
    