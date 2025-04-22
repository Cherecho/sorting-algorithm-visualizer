def quick_sort(array, update_callback):
    def partition(low, high):
        pivot = array[high]
        # Highlight the pivot element
        update_callback(array, highlight_indices=[high], moving_index=None)
        i = low - 1
        for j in range(low, high):
            # Highlight elements being compared
            update_callback(array, highlight_indices=[i + 1, j, high], moving_index=j)
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                # Highlight the swap
                update_callback(array, highlight_indices=[i, j, high], moving_index=j)

        # Place pivot in correct position
        array[i + 1], array[high] = array[high], array[i + 1]
        # Highlight the pivot's final position for this partition
        update_callback(array, highlight_indices=[i + 1], moving_index=i + 1)
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            # pi is partitioning index, array[p] is now at right place
            pi = partition(low, high)

            # Separately sort elements before partition and after partition
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(array) - 1)
    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(len(array)):
        update_callback(array, moving_index=i, end=True, sweep=True)
