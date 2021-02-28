import math
import os
from tabulate import tabulate


COLOR = {
    "PURPLE": '\033[95m',
    "CYAN": '\033[96m',
    "DARKCYAN": '\033[36m',
    "BLUE": '\033[94m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "RED": '\033[91m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m',
    "END": '\033[0m'
}

base_variables = ['x1', 'x2', 'f1', 'f2', 'a1', 'a2', 'a3']
non_base_variables = ['a1', 'a2', 'a3']

matrix = [
    [1.0, 6.0, -1.0, 0.0, 1.0, 0.0, 0.0],
    [4.0, 3.0, 0.0, -1.0, 0.0, 1.0, 0.0],
    [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0]
]

objective = [-15, -32, 0, 0, 0, 0, 0]

objective_aux = [-6, -11, 1, 1, 0, 0, 0]

total = 0

total_aux = -37

independent_terms = [7, 12, 18]

quotients = []


def is_optimum_solution(function):
    for number in function:
        if number < 0:
            return False
    return True


def get_pivot_column_index(function):
    return function.index(min(function))


def get_pivot_line_index(j):
    for i, term in enumerate(independent_terms):
        coefficient = matrix[i][j]
        if coefficient == 0:
            quotients.append(math.inf)
        else:
            quotients.append(term / coefficient)

    return quotients.index(min_positive(quotients.copy()))


def min_positive(iterable):
    iterable_aux = iterable.copy()
    for i, number in enumerate(iterable):
        if number <= 0:
            iterable[i] = math.inf

    try:
        if min(iterable) != math.inf:
            print("Min Division", min(iterable))
            return min(iterable)
        else:
            raise Exception('There is no minimum positive')
    except:
        print('No optimal solution')
        exit(1)


def reset_pivot_line():
    for i, number in enumerate(matrix[pivot_line_index]):
        if number != 0:
            matrix[pivot_line_index][i] = number / pivot_number

    if independent_terms[pivot_line_index] != 0:
        independent_terms[pivot_line_index] = independent_terms[pivot_line_index] / pivot_number


def scale_matrix():
    global total, total_aux
    for i, line in enumerate(matrix):
        if line[pivot_column_index] != 0 and i != pivot_line_index:
            div = -1 * line[pivot_column_index]
            for j, value in enumerate(line):
                matrix[i][j] = round(value + div * matrix[pivot_line_index][j], 5)
            independent_terms[i] = round(independent_terms[i] + div * independent_terms[pivot_line_index], 5)

    div = -1 * objective[pivot_column_index]

    for j, value in enumerate(objective):
        objective[j] = round(value + div * matrix[pivot_line_index][j], 5)

    total = round(total + div * independent_terms[pivot_line_index], 5)
    if not is_optimum_solution(objective_aux):
        div = -1 * objective_aux[pivot_column_index]

        for j, value in enumerate(objective_aux):
            objective_aux[j] = round(value + div * matrix[pivot_line_index][j], 5)

        total_aux = round(total_aux + div * independent_terms[pivot_line_index], 5)


def two_phase():
    remove_index = []
    for i, value in enumerate(base_variables):
        if 'a' in value:
            remove_index.append(i)

    for value in sorted(remove_index, reverse=True):
        base_variables.pop(value)
        objective.pop(value)

    for i, line in enumerate(matrix):
        for value in sorted(remove_index, reverse=True):
            matrix[i].pop(value)


def print_matrix(column=None, line=None):
    if not is_optimum_solution(objective_aux):
        lines = len(independent_terms) + 3
        columns = len(base_variables) + 2
        matrix_aux = lines * [columns * ['']]
        matrix_aux[0] = organize_line('\\', base_variables, 'b')
        for i in range(lines - 3):
            matrix_aux[i + 1] = organize_line(non_base_variables[i], matrix[i], independent_terms[i])
        matrix_aux[lines - 2] = organize_line('Z', objective, total)
        matrix_aux[lines - 1] = organize_line('Z\'', objective_aux, total_aux)
    else:
        lines = len(independent_terms) + 2
        columns = len(base_variables) + 2
        matrix_aux = lines * [columns * ['']]
        matrix_aux[0] = organize_line('\\', base_variables, 'b')
        for i in range(lines - 2):
            matrix_aux[i + 1] = organize_line(non_base_variables[i], matrix[i], independent_terms[i])
        matrix_aux[lines - 1] = organize_line('Z', objective, total)

    if column is None and line is None:
        print(tabulate(matrix_aux, headers='firstrow', tablefmt='fancy_grid'))
    else:
        line += 1
        column += 1
        for i in range(0, len(matrix_aux)):
            for j in range(0, len(matrix_aux[0])):
                if j == column and i == line:
                    matrix_aux[i][j] = f'{COLOR["BLUE"]}{COLOR["BOLD"]}{matrix_aux[i][j]}{COLOR["END"]}'
                elif i == line:
                    matrix_aux[i][j] = f'{COLOR["RED"]}{matrix_aux[i][j]}{COLOR["END"]}'
                elif j == column:
                    matrix_aux[i][j] = f'{COLOR["RED"]}{matrix_aux[i][j]}{COLOR["END"]}'

        print(tabulate(matrix_aux, headers='firstrow', tablefmt='fancy_grid'))
    print('\n\n')

def organize_line(non_base, values, independent):
    line = (len(base_variables) + 2) * ['']
    line[0] = str(non_base)
    for i, value in enumerate(values):
        line[i + 1] = str(values[i])
    line[len(values) + 1] = str(independent)
    return line


def init():

    print(
        "  _______                  _ _ _                _____       _                                   _____           _     _                 \n"
        " |__   __|                | | (_)              / ____|     | |                                 |  __ \         | |   | |                \n"
        "    | |_ __ __ ___   _____| | |_ _ __   __ _  | (___   __ _| | ___  ___ _ __ ___   __ _ _ __   | |__) | __ ___ | |__ | | ___ _ __ ___   \n"
        "    | | '__/ _` \ \ / / _ \ | | | '_ \ / _` |  \___ \ / _` | |/ _ \/ __| '_ ` _ \ / _` | '_ \  |  ___/ '__/ _ \| '_ \| |/ _ \ '_ ` _ \  \n"
        "    | | | | (_| |\ V /  __/ | | | | | | (_| |  ____) | (_| | |  __/\__ \ | | | | | (_| | | | | | |   | | | (_) | |_) | |  __/ | | | | | \n"
        "    |_|_|  \__,_| \_/ \___|_|_|_|_| |_|\__, | |_____/ \__,_|_|\___||___/_| |_| |_|\__,_|_| |_| |_|   |_|  \___/|_.__/|_|\___|_| |_| |_| \n"
        "                                        __/ |                                                                                           \n"
        "                                       |___/                                                                                            \n"
    )

    input(" PRESS ENTER TO START")
    os.system('cls')


init()
print(' Initial Table\n')
print_matrix()
print('\n======================================================================================================================\n')

while True:

    if not is_optimum_solution(objective_aux):
        pivot_column_index = get_pivot_column_index(objective_aux)
    elif not is_optimum_solution(objective):
        pivot_column_index = get_pivot_column_index(objective)

    print("Pivot Column Index", pivot_column_index)
    pivot_line_index = get_pivot_line_index(pivot_column_index)
    if pivot_line_index == -1:
        continue
    print("Pivot Line Index", pivot_line_index)
    pivot_number = matrix[pivot_line_index][pivot_column_index]
    print("Pivot Number", pivot_number)
    non_base_variables[pivot_line_index] = base_variables[pivot_column_index]
    print_matrix(pivot_column_index, pivot_line_index)
    reset_pivot_line()

    if not is_optimum_solution(objective_aux):
        scale_matrix()
    elif not is_optimum_solution(objective):
        scale_matrix()
    else:
        break

    quotients.clear()

    if is_optimum_solution(objective_aux):
        two_phase()


print('\n======================================================================================================================\n')
print(' Final Table\n')
print_matrix()
