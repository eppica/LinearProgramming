import math
from tabulate import tabulate

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
            iterable[i] = inf
        return min(iterable) if min(iterable) != math.inf else -1


def reset_pivot_line():
    for i, number in enumerate(matrix[pivot_line_index]):
        if number != 0:
            matrix[pivot_line_index][i] = number / pivot_number

    if independent_terms[pivot_line_index] != 0:
        independent_terms[pivot_line_index] = independent_terms[pivot_line_index] / pivot_number


def scale_matrix():
    global total
    for i, line in enumerate(matrix):
        if line[pivot_column_index] != 0 and i != pivot_line_index:
            div = -1 * line[pivot_column_index]
            for j, value in enumerate(line):
                matrix[i][j] = value + div * matrix[pivot_line_index][j]
            independent_terms[i] += div * independent_terms[pivot_line_index]

    div = -1 * objective[pivot_column_index]

    for j, value in enumerate(objective):
        objective[j] = value + div * matrix[pivot_line_index][j]

    total += div * independent_terms[pivot_line_index]


def print_matrix():
    lines = len(independent_terms) + 2
    columns = len(base_variables) + 2
    matrix_aux = lines * [columns * ['']]
    matrix_aux[0] = organize_line('\\', base_variables, 'b')
    for i in range(lines - 2):
        matrix_aux[i + 1] = organize_line(non_base_variables[i], matrix[i], independent_terms[i])
    matrix_aux[lines - 1] = organize_line('Z', objective, total)

    print(tabulate(matrix_aux, headers='firstrow', tablefmt='fancy_grid'))


def organize_line(non_base, values, independent):
    line = (len(base_variables) + 2) * ['']
    line[0] = str(non_base)
    for i, value in enumerate(values):
        line[i + 1] = str(values[i])
    line[len(values) + 1] = str(independent)
    return line


while not is_optimum_solution(objective):
    print_matrix()
    pivot_column_index = get_pivot_column_index(objective)
    print("Pivot_Column_Index", pivot_column_index)
    pivot_line_index = get_pivot_line_index(pivot_column_index)
    if pivot_line_index == -1:
        continue
    print("Pivot_Line_Index", pivot_line_index)
    pivot_number = matrix[pivot_line_index][pivot_column_index]
    print("Pivot_Number", pivot_number)
    non_base_variables[pivot_line_index] = base_variables[pivot_column_index]

    reset_pivot_line()

    scale_matrix()

    quotients.clear()

print_matrix()
