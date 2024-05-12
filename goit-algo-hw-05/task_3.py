import timeit
import statistics


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    pi = compute_prefix_function(pattern)
    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            return i - m + 1
    return -1


def rabin_karp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    if n < m:
        return -1

    # Хеш для шаблону і першого відрізку тексту
    pattern_hash = hash(pattern)
    text_hash = hash(text[:m])

    for i in range(n - m + 1):
        # Перевірка збігу хешу
        if pattern_hash == text_hash:
            if text[i:i+m] == pattern:
                return i
        # Перерахунок хешу для наступного відрізка
        if i < n - m:
            text_hash = hash(text[i+1:i+m+1])
    return -1


# Зчитуємо текстові файли
with open("article1.txt", "r") as file:
    text1 = file.read()
with open("article2.txt", "r") as file:
    text2 = file.read()

# Випадкові підрядки
pattern1 = "pattern1"
pattern1_real = "Жадібний алгоритм"
pattern2 = "pattern2"
pattern2_real = "експеримент"

repeat_count = 5

# Вимірюємо час для алгоритму Боєра-Мура
execution_times = timeit.repeat(lambda: boyer_moore_search(
    text1, pattern1_real), repeat=repeat_count, number=1000)
time_bm1_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: boyer_moore_search(
    text1, pattern1), repeat=repeat_count, number=1000)
time_bm1 = statistics.mean(execution_times)

execution_times = timeit.repeat(lambda: boyer_moore_search(
    text2, pattern2_real), repeat=repeat_count, number=1000)
time_bm2_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: boyer_moore_search(
    text2, pattern2), repeat=repeat_count, number=1000)
time_bm2 = statistics.mean(execution_times)

# Вимірюємо час для алгоритму Кнута-Морріса-Пратта
execution_times = timeit.repeat(lambda: kmp_search(
    text1, pattern1_real), repeat=repeat_count, number=1000)
time_kmp1_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: kmp_search(
    text1, pattern1), repeat=repeat_count, number=1000)
time_kmp1 = statistics.mean(execution_times)

execution_times = timeit.repeat(lambda: kmp_search(
    text2, pattern2_real), repeat=repeat_count, number=1000)
time_kmp2_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: kmp_search(
    text2, pattern2), repeat=repeat_count, number=1000)
time_kmp2 = statistics.mean(execution_times)

# Вимірюємо час для алгоритму Рабіна-Карпа
execution_times = timeit.repeat(lambda: rabin_karp_search(
    text1, pattern1_real), repeat=repeat_count, number=1000)
time_rk1_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: rabin_karp_search(
    text1, pattern1), repeat=repeat_count, number=1000)
time_rk1 = statistics.mean(execution_times)

execution_times = timeit.repeat(lambda: rabin_karp_search(
    text2, pattern2_real), repeat=repeat_count, number=1000)
time_rk2_real = statistics.mean(execution_times)
execution_times = timeit.repeat(lambda: rabin_karp_search(
    text2, pattern2), repeat=repeat_count, number=1000)
time_rk2 = statistics.mean(execution_times)

# Виводимо результати
print("Час виконання для алгоритму Боєра-Мура (Стаття 1 Існуючий текст):", time_bm1_real)
print("Час виконання для алгоритму Боєра-Мура (Стаття 1 Неіснуючий текст):", time_bm1)
print("Час виконання для алгоритму Боєра-Мура (Стаття 2 Існуючий текст):", time_bm2_real)
print("Час виконання для алгоритму Боєра-Мура (Стаття 2 Неіснуючий текст):", time_bm2)
print("Час виконання для алгоритму Кнута-Морріса-Пратта (Стаття 1 Існуючий текст):", time_kmp1_real)
print("Час виконання для алгоритму Кнута-Морріса-Пратта (Стаття 1 Неіснуючий текст):", time_kmp1)
print("Час виконання для алгоритму Кнута-Морріса-Пратта (Стаття 2 Існуючий текст):", time_kmp2_real)
print("Час виконання для алгоритму Кнута-Морріса-Пратта (Стаття 2 Неіснуючий текст):", time_kmp2)
print("Час виконання для алгоритму Рабіна-Карпа (Стаття 1 Існуючий текст):", time_rk1_real)
print("Час виконання для алгоритму Рабіна-Карпа (Стаття 1 Неіснуючий текст):", time_rk1)
print("Час виконання для алгоритму Рабіна-Карпа (Стаття 2 Існуючий текст):", time_rk2_real)
print("Час виконання для алгоритму Рабіна-Карпа (Стаття 2 Неіснуючий):", time_rk2)
