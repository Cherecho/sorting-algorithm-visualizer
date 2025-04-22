def radix_sort(array, update_callback):
    def counting_sort(array, exp):
        n = len(array)
        output = [0] * n
        count = [0] * 10

        # Store count of occurrences in count[]
        for i in range(n):
            index = array[i] // exp
            count[index % 10] += 1
            # Highlight element being read
            update_callback(array, highlight_indices=[i], moving_index=None)

        # Change count[i] so that count[i] now contains actual
        # position of this digit in output[]
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array
        i = n - 1
        while i >= 0:
            index = array[i] // exp
            output_idx = count[index % 10] - 1
            output[output_idx] = array[i]
            count[index % 10] -= 1
            # Highlight element being placed
            update_callback(array, highlight_indices=[i], moving_index=output_idx)
            i -= 1

        # Copy the output array to array[], so that array[] now
        # contains sorted numbers according to current digit
        for i in range(n):
            array[i] = output[i]
            # Show the array after this pass - highlight the element just placed
            update_callback(array, highlight_indices=[], moving_index=i)

    if not array:
        return  # Handle empty array

    max_element = max(array) if array else 0
    exp = 1
    while max_element // exp > 0:
        counting_sort(array, exp)
        exp *= 10

    update_callback(array)  # Final update before sweep

    # Final sweep animation
    for i in range(len(array)):
        update_callback(array, moving_index=i, end=True, sweep=True)
