"""Вопрос №3

На языке Python предложить алгоритм, который быстрее всего (по процессорным тикам) отсортирует данный ей массив чисел.
Массив может быть любого размера со случайным порядком чисел (в том числе и отсортированным). Объяснить, почему вы
считаете, что функция соответствует заданным критериям.
"""

from random import randint


def partition(array: list, left: int, right: int) -> tuple:
    pivot = array[left]
    l = left
    i = l

    while i <= right:
        if pivot > array[i]:
            l += 1
            array[i], array[l] = array[l], array[i]
            i += 1
        elif pivot < array[i]:
            array[i], array[right] = array[right], array[i]
            right -= 1
        else:
            i += 1

    array[left], array[l] = array[l], array[left]
    return l - 1, right + 1


def quick_sort(array: list) -> None:
    def wrapper(array: list, left: int, right: int) -> None:
        if left < right:
            rand_idx = randint(left, right)
            array[left], array[rand_idx] = array[rand_idx], array[left]
            m_left, m_right = partition(array, left, right)
            wrapper(array, left, m_left)
            wrapper(array, m_right, right)

    wrapper(array, 0, len(array) - 1)


"""Вывод:

Для сортировки массива чисел использую алгоритм быстрой сортировки (QuickSort) с случайным выбором опорного элемента 
и сортировкой вставкой для небольших подмассивов, в среднем работает за O(nlogn) в худшем за O(n^2), но с использованием 
случайного опорного элемента вероятность этого снижается. Он все равно будет медленнее встроенного sorted, так как 
последний реализован на C, сравнения приведены в tests. 
QuickSort на практике часто работает быстрее, чем mergesort, из-за меньшего числа сравнений. В лучших случаях он будет 
выполняться быстрее, чем другие виды сортировок, так что считаю, что функция соответствует заданным критериям.
"""