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

    return quotients.index(min_p(quotients))


def min_p(iterable):
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


while not is_optimum_solution(objective):

    pivot_column_index = get_pivot_column_index(objective)

    pivot_line_index = get_pivot_line_index(pivot_column_index)

    pivot_number = matrix[pivot_line_index][pivot_column_index]

    non_base_variables[pivot_line_index] = base_variables[pivot_column_index]

    reset_pivot_line()

    scale_matrix()

    quotients.clear()
