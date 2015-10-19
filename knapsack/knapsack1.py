# предметы (items) будем задавать
# следующим кортежем (item_cost, item_weight)
def knapsack_pseudopolinomial_solution(items, max_weigth):
    # ключ - цена набора
    # значение - [цена набора, вес набора]
    selection = {0: [0, 0]}

    for item in items:
        new_selection = []

        # по всем частичным решениям
        for solution in selection.values():
            new_solution = [solution[0] + item[0],  solution[1] + item[1]]

            # проверяем новое решение
            if (new_solution[1] <= max_weigth) \
                    and (new_solution[0] not in selection
                         or new_solution[1] < selection[new_solution[0]][1]):
                new_selection.append(new_solution)

        # регистрируем решения
        for solution in new_selection:
            selection[solution[0]] = solution

    return max(selection.keys())