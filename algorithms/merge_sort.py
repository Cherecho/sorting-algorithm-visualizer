def merge_sort(array, update_callback):
    def merge_sort_recursive(arr, temp, left_start, right_end):
        if left_start >= right_end:
            return

        middle = (left_start + right_end) // 2
        merge_sort_recursive(arr, temp, left_start, middle)
        merge_sort_recursive(arr, temp, middle + 1, right_end)
        merge(arr, temp, left_start, right_end)

    def merge(arr, temp, left_start, right_end):
        left_end = (right_end + left_start) // 2
        right_start = left_end + 1
        size = right_end - left_start + 1

        left = left_start
        right = right_start
        index = left_start

        highlight = list(range(left_start, right_end + 1))

        while left <= left_end and right <= right_end:
            # Highlight elements being compared
            update_callback(arr, highlight_indices=[left, right], moving_index=index)
            if arr[left] <= arr[right]:
                temp[index] = arr[left]
                left += 1
            else:
                temp[index] = arr[right]
                right += 1
            index += 1

        # Copy remaining elements from left half
        while left <= left_end:
            update_callback(arr, highlight_indices=[left], moving_index=index)
            temp[index] = arr[left]
            left += 1
            index += 1

        # Copy remaining elements from right half
        while right <= right_end:
            update_callback(arr, highlight_indices=[right], moving_index=index)
            temp[index] = arr[right]
            right += 1
            index += 1

        # Copy sorted elements back to original array
        for i in range(left_start, right_end + 1):
            arr[i] = temp[i]
            # Show the placement in the original array
            update_callback(arr, highlight_indices=[i], moving_index=i)

    n = len(array)
    temp_array = [0] * n
    merge_sort_recursive(array, temp_array, 0, n - 1)

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
