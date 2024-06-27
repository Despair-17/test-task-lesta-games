import timeit
from collections import deque
from random import randint
from time import perf_counter
from unittest import TestCase

from task1 import isEven, is_even
from task2 import CircularBufferList, CircularBufferNode
from task3 import quick_sort


class TestTask1(TestCase):

    def test_result(self):
        nums = range(-1000, 1001)
        for num in nums:
            self.assertEqual(isEven(num), is_even(num))

    def test_execution_time(self):
        nums = range(1_000_000, 2_000_000)

        def test_func(func, nums, repeats=100):
            total_time = 0
            for num in nums:
                single_run_time = 0
                for _ in range(repeats):
                    start_time = perf_counter()
                    func(num)
                    single_run_time += perf_counter() - start_time
                total_time += single_run_time / repeats
            return total_time / len(nums)

        time_even_mod = test_func(isEven, nums)
        time_even_bit = test_func(is_even, nums)

        self.assertGreater(time_even_mod, time_even_bit)


class TestTask2(TestCase):

    def test_cir_buffer_init_list(self):
        test_data = ((15, 10), (10, 10), (0, 10))

        for count_num, size in test_data:
            nums = range(count_num)
            deq = deque(nums, maxlen=size)
            cir_buffer_list = CircularBufferList(iterable=nums, size=size)
            cir_buffer_node = CircularBufferNode(iterable=nums, size=size)
            list_deq = list(deq)
            self.assertEqual(list_deq, list(cir_buffer_list))
            self.assertEqual(list_deq, list(cir_buffer_node))

    def test_cir_buffer_results_list(self):
        test_command = [
            "append",
            "append",
            "append",
            "append",
            "append",
            "append",
            "popleft",
            "append",
            "append",
            "append",
            "append",
            "popleft",
            "popleft",
            "popleft",
            "popleft",
            "popleft",
            "append",
            "popleft",
        ]
        test_data = [(item, command) for item, command in enumerate(test_command)]

        iterable, size = [], 5
        deq = deque(iterable, maxlen=size)
        cir_buffer_list = CircularBufferList(iterable, size=size)
        cir_buffer_node = CircularBufferNode(iterable, size=size)

        for item, command in test_data:
            if command == "append":
                deq.append(item)
                cir_buffer_list.append(item)
                cir_buffer_node.append(item)
            elif command == "popleft":
                item_deque = deq.popleft()
                item_cir_buffer_list = cir_buffer_list.popleft()
                item_cir_buffer_node = cir_buffer_node.popleft()

                self.assertEqual(item_deque, item_cir_buffer_list)
                self.assertEqual(item_deque, item_cir_buffer_node)

            list_deq = list(deq)
            self.assertEqual(list_deq, list(cir_buffer_list))
            self.assertEqual(list_deq, list(cir_buffer_node))


def generate_random_array(size: int) -> list[int]:
    return [randint(0, 1000000) for _ in range(size)]


class TestTask3(TestCase):

    def test_correctness(self):
        arrays = [
            [],
            [1],
            [2, 1],
            [1, 2, 3],
            [3, 2, 1],
            [6, 3, 3, 1, 5, 6],
            generate_random_array(100),
            generate_random_array(1000),
        ]

        for array in arrays:
            with self.subTest(array=array):
                sorted_array = sorted(array)
                quick_sort(array)
                self.assertEqual(array, sorted_array)

    def test_performance(self):
        sizes = [1000, 10000, 100000, 1000000]

        for size in sizes:
            array = generate_random_array(size)
            qs_time = timeit.timeit(lambda: quick_sort(array[:]), number=1)
            sorted_time = timeit.timeit(lambda: sorted(array[:]), number=1)
            print(f"QuickSort with array size {size}: {qs_time:.6f} seconds")
            print(f"sorted() with array size {size}: {sorted_time:.6f} seconds")
