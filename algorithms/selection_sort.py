def selection_sort(array, update_callback):
    n = len(array)
    for i in range(n):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        # Highlight the start of the unsorted section
        update_callback(array, highlight_indices=[i], moving_index=None)

        for j in range(i + 1, n):
            # Highlight current minimum and element being compared
            update_callback(array, highlight_indices=[i, min_idx], moving_index=j)
            if array[j] < array[min_idx]:
                min_idx = j
                # Highlight the new minimum found
                update_callback(array, highlight_indices=[i, min_idx], moving_index=j)

        # Swap the found minimum element with the first element
        array[i], array[min_idx] = array[min_idx], array[i]
        # Highlight the swap into the sorted position
        update_callback(array, highlight_indices=[i], moving_index=min_idx)

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
