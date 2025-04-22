# Sorting Algorithm Visualizer

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python application using Pygame to visualize various sorting algorithms in action. Features include an interactive startup menu, adjustable speed, sound feedback for element access/movement, and fullscreen support.

![Sorting Visualizer Demo GIF](./assets/visualizer_demo.gif)

## Features

*   **Interactive Startup Menu:** Configure the visualization (algorithm, array size, max value, speed, uniqueness) through a simple text menu when the application starts.
*   **Multiple Algorithms:** Visualize classic sorting algorithms.
*   **Visual Feedback:** Bars represent array elements, colored based on value and status (comparing, moving, sorted).
*   **Auditory Feedback:** Distinct sounds play when elements are accessed or moved, with pitch corresponding to the element's value.
*   **Speed Control:** Adjust the visualization speed dynamically using keyboard shortcuts *during* the visualization.
*   **Pause/Resume:** Pause the visualization at any point.
*   **Fullscreen Mode:** Toggle between windowed and fullscreen display.
*   **Dynamic Algorithm Loading:** Easily add new sorting algorithms by placing them in the `algorithms` directory.
*   **Robust Error Handling:** Gracefully handles common errors during setup and visualization.

## Available Algorithms

The visualizer automatically detects algorithms placed in the `algorithms/` directory. Currently included:

*   `bubble_sort`
*   `selection_sort`
*   `insertion_sort`
*   `quick_sort`
*   `heap_sort`
*   `radix_sort`
*   `merge_sort`
*   `shell_sort`

## Requirements

*   Python 3.7+
*   Pygame: `pip install pygame`
*   NumPy: `pip install numpy`

You can install all requirements using:
```bash
pip install -r requirements.txt
```
*(Ensure you have a `requirements.txt` file containing `pygame` and `numpy`)*

## Usage

1.  **Navigate:** Open your terminal or command prompt and navigate to the project's root directory (the one containing `main.py` and the `algorithms/` folder).
2.  **Run:** Execute the main script:
    ```bash
    python main.py
    ```
3.  **Configure:** Follow the prompts in the terminal to:
    *   Choose the sorting algorithm from the list.
    *   Enter the desired array size (number of elements).
    *   Enter the maximum value for elements in the array.
    *   Enter the initial delay between visualization steps (in milliseconds - lower is faster).
    *   Choose whether to generate unique elements.
4.  **Visualize:** Once configured, the Pygame window will launch and the visualization will begin.

## Controls (During Visualization)

*   `+` / `=` / Numpad `+`: Increase delay (slow down).
*   `-` / Numpad `-`: Decrease delay (speed up).
*   `P`: Pause / Resume the visualization.
*   `ESC`: Toggle fullscreen mode.
*   `R`: Restart the current visualization with the same settings.
*   `Q`: Quit the application immediately.

## Adding New Algorithms

1.  Create a new Python file in the `algorithms/` directory (e.g., `my_cool_sort.py`).
2.  Inside the file, define a function with the *exact same name* as the file (e.g., `def my_cool_sort(array, update_callback):`).
3.  Implement your sorting algorithm within this function.
4.  Call the `update_callback` function whenever you want the display to refresh. Pass the current state of the `array` and optionally `highlight_indices` (list of indices to color differently) and `moving_index` (index of the element currently being moved/placed/compared). Use `sweep=True` in the final pass.
    *   `update_callback(array, highlight_indices=[i, j], moving_index=k)`
    *   `update_callback(array, moving_index=i, end=True, sweep=True)` # For final sweep
5.  The new algorithm (`my_cool_sort`) will automatically appear in the startup menu the next time you run `python main.py`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.