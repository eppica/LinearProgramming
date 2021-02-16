import math

base_variables = ['x1', 'x2', 'f1', 'f2', 'f3']
non_base_variables = ['f1', 'f2', 'f3']

matrix = [
    [1, 0, 1, 0, 0],
    [0, 2, 0, 1, 0],
    [2, 3, 0, 0, 1]
]

objective = [-3, -5, 0, 0, 0]

total = 0

independent_terms = [4, 12, 21]

quocients = []


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
            quocients.append(math.inf)
        else:
            quocients.append(term / coefficient)

    return quocients.index(min(quocients))


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
            div = line[pivot_column_index]
            for j, value in enumerate(line):
                if div > 0:
                    matrix[i][j] = value - abs(div) * matrix[pivot_line_index][j]
                else:
                    matrix[i][j] = value + abs(div) * matrix[pivot_line_index][j]
            if div > 0:
                independent_terms[i] -= abs(div) * independent_terms[pivot_line_index]
            else:
                independent_terms[i] += abs(div) * independent_terms[pivot_line_index]

    div = objective[pivot_column_index]

    for j, value in enumerate(objective):
        if div > 0:
            objective[j] = value - abs(div) * matrix[pivot_line_index][j]
        else:
            objective[j] = value + abs(div) * matrix[pivot_line_index][j]

    if div > 0:
        total -= abs(div) * independent_terms[pivot_line_index]
    else:
        total += abs(div) * independent_terms[pivot_line_index]


while not is_optimum_solution(objective):

    pivot_column_index = get_pivot_column_index(objective)

    pivot_line_index = get_pivot_line_index(pivot_column_index)

    pivot_number = matrix[pivot_line_index][pivot_column_index]

    non_base_variables[pivot_line_index] = base_variables[pivot_column_index]

    reset_pivot_line()

    scale_matrix()

    quocients.clear()
