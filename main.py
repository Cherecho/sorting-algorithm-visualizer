import displayer as displayer
from displayer import RestartAlgorithm
import random
import sys
import os
import time
import traceback  # Import traceback for better error printing
import pygame

ALGORITHMS = (
    {}
)  # Will store {'name': {'func': <func>, 'avg': 'O(..)', 'best': 'O(..)', 'rank': N}}
algo_path = os.path.join(os.path.dirname(__file__), "algorithms")
if not os.path.isdir(algo_path):
    if "__file__" in globals():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        algo_path = os.path.join(script_dir, "algorithms")
if not os.path.isdir(algo_path):
    print(
        f"Error: Cannot find the 'algorithms' directory at expected location: {algo_path}"
    )
    sys.exit(1)
sys.path.insert(0, algo_path)
ALGO_COMPLEXITY_DATA = {
    "merge_sort": {"avg": "O(n log n)", "best": "O(n log n)", "rank": 2},
    "heap_sort": {"avg": "O(n log n)", "best": "O(n log n)", "rank": 2},
    "quick_sort": {
        "avg": "O(n log n)",
        "best": "O(n log n)",
        "rank": 2,
        "worst": "O(n^2)",
    },
    "insertion_sort": {"avg": "O(n^2)", "best": "O(n)", "rank": 4},
    "bubble_sort": {"avg": "O(n^2)", "best": "O(n)", "rank": 4},
    "selection_sort": {"avg": "O(n^2)", "best": "O(n^2)", "rank": 4},
    "shell_sort": {"avg": "~O(n log^2 n)", "best": "O(n log n)", "rank": 3},
    "radix_sort": {"avg": "O(nk)", "best": "O(nk)", "rank": 1},
}
algo_files = [
    f for f in os.listdir(algo_path) if f.endswith(".py") and not f.startswith("__")
]
available_algo_names = sorted([f[:-3] for f in algo_files])
for module_name in available_algo_names:
    try:
        module = __import__(module_name)
        if hasattr(module, module_name):
            func = getattr(module, module_name)
            complexity_info = ALGO_COMPLEXITY_DATA.get(module_name)
            if complexity_info:
                ALGORITHMS[module_name] = {
                    "func": func,
                    "avg": complexity_info["avg"],
                    "best": complexity_info["best"],
                    "rank": complexity_info["rank"],
                }
                if "worst" in complexity_info:
                    ALGORITHMS[module_name]["worst"] = complexity_info["worst"]
            else:
                print(f"Warning: Complexity data missing for '{module_name}'.")
                ALGORITHMS[module_name] = {
                    "func": func,
                    "avg": "O(?)",
                    "best": "O(?)",
                    "rank": 99,
                }
        else:
            print(
                f"Warning: Could not find function '{module_name}' in module '{module_name}.py'"
            )
    except ImportError as e:
        print(f"Error importing algorithm '{module_name}': {e}")
if algo_path in sys.path:
    sys.path.remove(algo_path)
if not ALGORITHMS:
    print("Error: No valid sorting algorithms found.")
    sys.exit(1)


def get_int_input(prompt, default_value):
    while True:
        try:
            value_str = input(f"{prompt} (default: {default_value}): ")
            if not value_str:
                return default_value
            value = int(value_str)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_choice_input(prompt, algorithms_data, default_key=None):
    print(prompt)
    sorted_algo_names = sorted(
        algorithms_data.keys(), key=lambda name: (algorithms_data[name]["rank"], name)
    )
    default_index = -1
    if default_key and default_key in sorted_algo_names:
        try:
            default_index = sorted_algo_names.index(default_key)
        except ValueError:
            default_index = -1
    max_name_len = (
        max(len(name) for name in sorted_algo_names) if sorted_algo_names else 0
    )
    for i, name in enumerate(sorted_algo_names):
        info = algorithms_data[name]
        complexity_str = f"(Avg: {info['avg']}, Best: {info['best']})"
        default_marker = " (default)" if i == default_index else ""
        print(
            f"  {i+1}. {name.replace('_', ' ').title():<{max_name_len+1}} {complexity_str}{default_marker}"
        )
    while True:
        try:
            default_prompt_val = str(default_index + 1) if default_index != -1 else ""
            choice_str = input(
                f"Enter choice (1-{len(sorted_algo_names)}) [{default_prompt_val}]: "
            )
            if not choice_str and default_index != -1:
                return sorted_algo_names[default_index]
            choice_num = int(choice_str)
            if 1 <= choice_num <= len(sorted_algo_names):
                return sorted_algo_names[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(sorted_algo_names)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# --- End Helper Functions ---


# --- display_menu_and_get_settings (remains the same) ---
def display_menu_and_get_settings():
    print("\n--- Sorting Algorithm Visualizer ---")
    preferred_default = (
        "merge_sort" if "merge_sort" in ALGORITHMS else list(ALGORITHMS.keys())[0]
    )
    selected_algo_name = get_choice_input(
        "Choose Algorithm:", ALGORITHMS, default_key=preferred_default
    )
    array_size = get_int_input("Enter Array Size", default_value=100)
    max_value = get_int_input("Enter Max Element Value", default_value=500)
    initial_delay = get_int_input("Enter Initial Delay (ms)", default_value=5)
    unique_choice = (
        input("Generate Unique Elements? (y/N, default: N): ").strip().lower()
    )
    use_unique = unique_choice == "y"
    print("\nSettings Chosen:")
    print(f"- Algorithm: {selected_algo_name.replace('_', ' ').title()}")
    print(f"- Array Size: {array_size}")
    print(f"- Max Value: {max_value}")
    print(f"- Delay: {initial_delay} ms")
    print(f"- Unique Elements: {'Yes' if use_unique else 'No'}")
    print("-" * 20)
    time.sleep(1)
    return {
        "algorithm": selected_algo_name,
        "size": array_size,
        "max_value": max_value,
        "delay": initial_delay,
        "unique": use_unique,
    }


def main():
    settings = display_menu_and_get_settings()

    # Store initial generation settings
    initial_max_value = settings["max_value"]
    initial_size = settings["size"]
    initial_unique = settings["unique"]

    # Validate settings
    if initial_unique and initial_size > initial_max_value:
        print(
            f"\nWarning: Cannot generate {initial_size} unique values from range 1 to {initial_max_value}. Reducing size to {initial_max_value}."
        )
        initial_size = initial_max_value
        if initial_size <= 0:
            print("Error: Cannot proceed with size 0 after adjustment.")
            sys.exit(1)
        settings["size"] = (
            initial_size  # Update settings dict for consistency if needed
        )
        time.sleep(1)

    # Helper to create array instance
    def create_array_instance():
        if initial_unique:
            try:
                return random.sample(range(1, initial_max_value + 1), initial_size)
            except ValueError as e:
                print(f"\nError generating unique sample: {e}")
                sys.exit(1)
        else:
            return [random.randint(1, initial_max_value) for _ in range(initial_size)]

    # Get algorithm details
    selected_algo_details = ALGORITHMS.get(settings["algorithm"])
    if not selected_algo_details:
        print(
            f"Error: Algorithm '{settings['algorithm']}' implementation details not found."
        )
        sys.exit(1)
    sorting_algorithm = selected_algo_details["func"]

    display = None
    keep_running_app = True  # Controls the outer restart loop

    while keep_running_app:
        current_array = create_array_instance()
        is_first_run = display is None  # Check if display needs initialization

        try:
            if is_first_run:
                # Initialize Pygame Display (only once)
                print(f"\nInitializing Pygame and starting visualization...")
                print(
                    "Controls: [P] Pause | [R] Restart | [+/-] Speed | [ESC] Fullscreen | [Q] Quit"
                )
                display = displayer.Displayer(
                    current_array,  # Pass the first array instance
                    algorithm_name=settings["algorithm"],
                    delay_ms=settings["delay"],
                )
            else:
                # Reset display state for subsequent runs
                print("\nResetting and restarting visualization...")
                display.original_array = list(
                    current_array
                )  # Update displayer's original array
                display.reset_array()  # Resets display's internal array and redraws
                display.reset_timer()  # Resets display's timer

            sorting_algorithm(current_array, display.update)

            print("\nSorting complete. Displaying final result.")
            print("Press Q or close the window to exit. Press R to restart.")
            # finalize() now also listens for 'R' and raises RestartAlgorithm
            display.finalize()

            print("\nFinalize completed without restart request.")
            keep_running_app = False  # Exit the outer while loop

        except RestartAlgorithm:
            print("Restarting visualization...")
            time.sleep(0.1)  # Small pause
            continue

        except (KeyboardInterrupt, SystemExit):
            print("\nExiting gracefully...")
            keep_running_app = False

        except Exception as e:
            print(f"\n--- An Unexpected Error Occurred ---")
            traceback.print_exc()  # Print detailed traceback
            print(f"Error details: {e}")
            print("------------------------------------")
            keep_running_app = False  # Stop loop on other errors

    print("\nExiting Sorting Visualizer.")
    # Ensure Pygame is quit cleanly
    if pygame.get_init():
        try:
            pygame.quit()
        except Exception as quit_err:
            print(f"Error during Pygame quit: {quit_err}")


if __name__ == "__main__":
    if sys.stdout is None or sys.stdin is None:
        print("Error: Standard input/output not available for menu setup.")
        sys.exit(1)

    main()
