import math
import os
from tabulate import tabulate

M = 999

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

base_variables = ['x1', 'x2', 'f1', 'f2', 'f3']
non_base_variables = ['f1', 'f2', 'f3']

matrix = [
    [1.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 2.0, 0.0, 1.0, 0.0],
    [2.0, 3.0, 0.0, 0.0, 1.0]
]

objective = [-3, -5, 0, 0, 0]

total = 0

independent_terms = [4, 12, 21]

quotients = []


def big_m():
    global total
    div = -1 * M

    for i, base in enumerate(non_base_variables):
        if 'a' in base:

            for j in rand(0, len(objective)):
                objective[j] = round(objective[j] + div * matrix[i][j], 5)

            total = round(total + div * independent_terms[i], 5)


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

    return quotients.index(min_positive(quotients))


def min_positive(iterable):
    for i, number in enumerate(iterable):
        if number < 0:
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
        matrix[pivot_line_index][i] = number / pivot_number

    independent_terms[pivot_line_index] = independent_terms[pivot_line_index] / pivot_number


def scale_matrix():
    global total
    for i, line in enumerate(matrix):
        if i != pivot_line_index:
            div = -1 * line[pivot_column_index]
            for j, value in enumerate(line):
                matrix[i][j] = round(value + div * matrix[pivot_line_index][j], 5)
            independent_terms[i] = round(independent_terms[i] + div * independent_terms[pivot_line_index], 5)

    div = -1 * objective[pivot_column_index]

    for j in rand(0, len(objective)):
        objective[j] = round(objective[j] + div * matrix[pivot_line_index][j], 5)

    total = round(total + div * independent_terms[pivot_line_index], 5)


def print_matrix(column=None, line=None):

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


# init()
print(' Initial Table\n')
print_matrix()
print('\n======================================================================================================================\n')

big_m()

while True:

    if not is_optimum_solution(objective):
        pivot_column_index = get_pivot_column_index(objective)

        print("Pivot Column Index", pivot_column_index)

        pivot_line_index = get_pivot_line_index(pivot_column_index)
        print("Pivot Line Index", pivot_line_index)

        pivot_number = matrix[pivot_line_index][pivot_column_index]
        print("Pivot Number", pivot_number)

        non_base_variables[pivot_line_index] = base_variables[pivot_column_index]

        print_matrix(pivot_column_index, pivot_line_index)

        reset_pivot_line()

        scale_matrix()
    else:
        break

    quotients.clear()


print('\n\n\n======================================================================================================================\n')
print(' Final Table\n')
print_matrix()
