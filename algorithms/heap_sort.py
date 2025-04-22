def heap_sort(array, update_callback):
    def heapify(n, i, arr_copy):  # Pass arr_copy for visualization consistency
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        # Highlight the root being considered for heapify
        update_callback(arr_copy, highlight_indices=[i], moving_index=None)

        # See if left child exists and is greater than root
        if l < n:
            # Highlight comparison
            update_callback(arr_copy, highlight_indices=[i, l], moving_index=l)
            if array[l] > array[largest]:
                largest = l

        # See if right child exists and is greater than largest so far
        if r < n:
            # Highlight comparison
            update_callback(arr_copy, highlight_indices=[i, largest, r], moving_index=r)
            if array[r] > array[largest]:
                largest = r

        # Change root, if needed
        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            # Highlight the swap during heapify
            arr_copy[:] = array  # Update visualization copy
            update_callback(
                arr_copy, highlight_indices=[i, largest], moving_index=largest
            )
            # Heapify the root.
            heapify(n, largest, arr_copy)

    n = len(array)
    vis_array = list(array)  # Use a copy for consistent visualization during heapify

    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i, vis_array)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        # Move current root to end
        array[i], array[0] = array[0], array[i]
        # Highlight the swap (moving max element to sorted position)
        vis_array[:] = array  # Update visualization copy
        update_callback(vis_array, highlight_indices=[0, i], moving_index=i)

        # call max heapify on the reduced heap
        heapify(i, 0, vis_array)

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
