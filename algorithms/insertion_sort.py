def insertion_sort(array, update_callback):
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        # Highlight the key element being considered
        update_callback(array, highlight_indices=[i], moving_index=i)

        # Move elements of array[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            # Highlight comparison and the element being shifted
            update_callback(array, highlight_indices=[j, i], moving_index=j + 1)
            j -= 1
        array[j + 1] = key
        # Highlight the final position where the key was inserted
        update_callback(array, highlight_indices=[j + 1], moving_index=j + 1)

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
