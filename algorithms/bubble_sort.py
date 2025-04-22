def bubble_sort(array, update_callback):
    n = len(array)
    swapped = True
    pass_num = 0
    while swapped:
        swapped = False
        for j in range(0, n - pass_num - 1):
            # Highlight compared elements
            update_callback(array, highlight_indices=[j, j + 1], moving_index=None)
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
                # Highlight swapped elements, moving_index shows the rightmost element involved
                update_callback(array, highlight_indices=[j, j + 1], moving_index=j + 1)
        pass_num += 1
        if not swapped:
            break

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
