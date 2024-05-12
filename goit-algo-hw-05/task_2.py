def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0

    while left <= right:
        mid = left + (right - left) // 2
        iterations += 1

        if arr[mid] < target:
            left = mid + 1
        elif arr[mid] > target:
            right = mid - 1
        else:
            return iterations, arr[mid]

    # Якщо елемент не знайдено, повертаємо "верхню межу"
    if right < 0:
        return iterations, arr[0]
    if left >= len(arr):
        return iterations, None
    return iterations, arr[left]

# Приклад використання
arr = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
target = 0.6
result = binary_search(arr, target)
print("Кількість ітерацій:", result[0])
print("Верхня межа:", result[1])
