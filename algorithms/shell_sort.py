def shell_sort(array, update_callback):
    n = len(array)
    # Start with a large gap, then reduce the gap
    # Using Knuth's sequence: h = h * 3 + 1 -> ..., 40, 13, 4, 1
    gap = 1
    while gap < n / 3:
        gap = gap * 3 + 1

    while gap > 0:
        # Do a gapped insertion sort for this gap size.
        # The first gap elements a[0..gap-1] are already in gapped order
        # keep adding one more element until the entire array is gap sorted
        for i in range(gap, n):
            # add a[i] to the elements that have been gap sorted
            # save a[i] in temp and make a hole at position i
            temp = array[i]

            # shift earlier gap-sorted elements up until the correct location for a[i] is found
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                # Highlight comparison and movement
                update_callback(array, highlight_indices=[j, j - gap], moving_index=j)
                j -= gap

            # put temp (the original a[i]) in its correct location
            array[j] = temp
            update_callback(
                array, highlight_indices=[i], moving_index=j
            )  # Show final placement

        # Reduce the gap
        gap = gap // 3  # Integer division is fine here

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(n):
        update_callback(array, moving_index=i, end=True, sweep=True)
