import sys
# псевдополиномиальное решение
# методом динамического программирования
def knapsack_pseudopolinomial_solution(items, max_weigth):
    # ключ - суммарная цена набора
    # значение - [цена набора, вес набора, номер последнего предмета]
    selection = {0: [0, 0, -1]}

    # сохраняем историю, для восстановления индексов наборов
    selection_history = [selection]

    for item in items:
        new_selection = []

        # по всем частичным решениям
        for solution in selection.values():
            new_solution = [solution[0] + item[0],  solution[1] + item[1], item[2]]

            # проверяем новое решение
            if (new_solution[1] <= max_weigth) \
                    and (new_solution[0] not in selection
                         or new_solution[1] < selection[new_solution[0]][1]):
                new_selection.append(new_solution)

        # регистрируем решения
        for solution in new_selection:
            selection[solution[0]] = solution

        # запоминаем текущие наборы для каждой стоимости
        selection_history.append(selection)

    # номера предметов оптимального набора
    indices = []

    solution = selection[max(selection.keys())]

    # восстановление набора
    while solution[2] != -1:
        indices.append(solution[2])
        solution = selection_history[solution[2]][solution[0] - items[solution[2]][0]]

    return indices


# полиномиальный приближенный алгоритм с точностью epsilon
def knapsack_approximated_solution(items, epsilon, max_weigth):
    # Вычисляем cmax
    low_cost = max(0, max(item[0] for item in items if item[1] <= max_weigth))

    if low_cost == 0:
        return 0

    # Вычисляем делитель для масштабирования весов
    alpha = max(1, epsilon * low_cost / (len(items) * (1 + epsilon)))

    # Масштабируем веса
    new_items = [(item[0]//alpha, item[1], item[2]) for item in items]

    # Вызываем решение динамическим программированием
    indices = knapsack_pseudopolinomial_solution(new_items, max_weigth)

    return sum([items[index][0] for index in indices])


def check_result(result, eps):
    file2 = open(sys.argv[3], 'r')
    answer = int(file2.readline())
    file2.close()

    if (result * (1 + eps) >= answer) and (result <= answer * (1 + eps)):
        return True
    else:
        return False


def time_count_decorator(function):
    def wrap(*args, **kwargs):
        import time
        start_time = time.clock()

        result_function = function(*args, **kwargs)

        print(time.clock() - start_time)
        return result_function

    return wrap

# параметры запуска:
# путь к входному файлу, epsilon, путь к файлу с ответом
if __name__ == "__main__":
    # точность, 0 равносильно выполнению
    # псевдополиномиального алгоритма
    epsilon = float(sys.argv[2])

    # список всех предметов
    items = []

    file1 = open(sys.argv[1], 'r')

    # ограничение размера рюкзака
    B = int(file1.readline())

    weights = file1.readline().split()
    costs = file1.readline().split()

    file1.close()

    # в нижеприведенном коде предметы будем задавать
    # следующим кортежем (item_cost, item_weight, item_number)
    for i in range(len(costs)):
        items.append((int(costs[i]), int(weights[i]), i))

    if check_result(time_count_decorator(knapsack_approximated_solution)(items, epsilon, B), epsilon):
        print("correct answer")
    else:
        print("wrong answer")
