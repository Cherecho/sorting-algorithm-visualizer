import pygame
import math
import time
from sound_manager import SoundManager


class RestartAlgorithm(Exception):
    """Custom exception to signal algorithm restart."""

    pass


class Displayer:
    """
    A class to visualize sorting algorithms using Pygame.
    Attributes:
        original_array (list): The original unsorted array.
        algorithm_name (str): The name of the sorting algorithm.
        width (int): The width of the display window.
        height (int): The height of the display window.
        screen (pygame.Surface): The Pygame display surface.
        fullscreen (bool): A flag indicating whether the display is in fullscreen mode.
        bg_color (tuple): The background color of the display.
        bar_start_color (tuple): The starting color of the bars.
        bar_end_color (tuple): The ending color of the bars.
        highlight_color (tuple): The color used to highlight bars during comparison.
        moving_color (tuple): The color used to indicate a bar is being moved.
        final_sweep_color (tuple): The color used during the final sweep of a sorting algorithm.
        text_color (tuple): The color of the text displayed on the screen.
        title_color (tuple): The color of the title text.
        font (pygame.font.Font): The font used for displaying text.
        title_font (pygame.font.Font): The font used for the title.
        array (list): The current state of the array being sorted.
        n (int): The number of elements in the array.
        max_value (int): The maximum value in the array.
        bar_area_height (int): The height of the area where bars are drawn.
        start_time (float): The time when the sorting started.
        elapsed_time (float): The time elapsed since the sorting started.
        running (bool): A flag indicating whether the visualization is running.
        paused (bool): A flag indicating whether the visualization is paused.
        restart_requested (bool): A flag indicating whether a restart has been requested.
        sound_manager (SoundManager): An instance of the SoundManager class for playing sounds.
        delay_ms (int): The delay in milliseconds between each update.
        min_delay (int): The minimum allowed delay.
        max_delay (int): The maximum allowed delay.
    Methods:
        __init__(self, array, algorithm_name="Unknown Algorithm", delay_ms=1):
            Initializes the Displayer with the given array, algorithm name, and delay.
        _get_bar_color(self, index, value, highlight_indices=[], moving_index=None, sweep=False):
            Determines the color of a bar based on its index, value, and other flags.
        toggle_fullscreen(self):
            Toggles between fullscreen and windowed mode.
        _draw_info_text(self, end, final_screen=False):
            Draws the algorithm title, timer, and control hints on the screen.
        _draw_frame(self, highlight_indices=[], moving_index=None, end=False, sweep=False, final_screen=False):
            Draws a single frame of the visualization, including bars and info text.
        _handle_events(self):
            Handles user input events such as quitting, toggling fullscreen, pausing, and restarting.
        reset_timer(self):
            Resets the timer to zero.
        reset_array(self):
            Resets the array to its original state and redraws the screen.
        update(self, array, highlight_indices=[], moving_index=None, end=False, sweep=False):
            Updates the display with the current state of the array and highlights.
        finalize(self):
            Keeps the final sorted state displayed until user action.
    """

    def __init__(self, array, algorithm_name="Unknown Algorithm", delay_ms=1):
        if not pygame.get_init():
            pygame.init()
        self.original_array = list(array)
        self.algorithm_name = algorithm_name.replace("_", " ").title()
        try:
            info = pygame.display.Info()
            self.width = info.current_w
            self.height = info.current_h
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF
            )
            self.fullscreen = True
        except pygame.error:
            print("Could not get display info, using default resolution.")
            self.width = 1280
            self.height = 720
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF
            )
            self.fullscreen = False
        pygame.display.set_caption(f"Sorting Visualizer - {self.algorithm_name}")
        self.bg_color = (20, 20, 30)
        self.bar_start_color = (50, 150, 255)
        self.bar_end_color = (255, 100, 150)
        self.highlight_color = (255, 255, 0)
        self.moving_color = (255, 50, 50)
        self.final_sweep_color = (0, 255, 100)
        self.text_color = (220, 220, 220)
        self.title_color = (255, 255, 255)
        try:
            self.font = pygame.font.SysFont("Consolas", 24)
            self.title_font = pygame.font.SysFont("Consolas", 36, bold=True)
        except Exception as e:
            print(f"Warning: Font loading error ({e}). Using Arial.")
            self.font = pygame.font.SysFont("Arial", 24)
            self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.array = list(self.original_array)
        self.n = len(self.array)
        self.max_value = max(self.array) if self.array else 1
        self.bar_area_height = self.height - 70
        self.start_time = time.time()
        self.elapsed_time = 0
        self.running = True
        self.paused = False
        self.restart_requested = False
        self.sound_manager = SoundManager(self.max_value)
        self.delay_ms = delay_ms
        self.min_delay = 0
        self.max_delay = 200
        self._draw_frame()  # Initial draw

    def _get_bar_color(
        self, index, value, highlight_indices=[], moving_index=None, sweep=False
    ):
        if sweep and index == moving_index:
            return self.final_sweep_color
        if index == moving_index:
            return self.moving_color
        elif index in highlight_indices:
            return self.highlight_color
        else:
            ratio = value / self.max_value if self.max_value > 0 else 0
            red = int(
                self.bar_start_color[0] * (1 - ratio) + self.bar_end_color[0] * ratio
            )
            green = int(
                self.bar_start_color[1] * (1 - ratio) + self.bar_end_color[1] * ratio
            )
            blue = int(
                self.bar_start_color[2] * (1 - ratio) + self.bar_end_color[2] * ratio
            )
            return (
                max(0, min(255, red)),
                max(0, min(255, green)),
                max(0, min(255, blue)),
            )  # Clamp colors

    def toggle_fullscreen(self):
        current_caption = pygame.display.get_caption()[0]
        pygame.display.quit()
        pygame.display.init()
        if not pygame.mixer.get_init():  # Re-init mixer
            try:
                pygame.mixer.init(
                    frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512
                )
                pygame.mixer.set_num_channels(32)
            except pygame.error as e:
                print(f"Warning: Failed to re-initialize Pygame Mixer: {e}")
        if self.fullscreen:  # Go windowed
            try:
                info = pygame.display.Info()
                default_w = max(1024, int(info.current_w * 0.75))
                default_h = max(768, int(info.current_h * 0.75))
            except:
                default_w, default_h = 1280, 720
            self.screen = pygame.display.set_mode(
                (default_w, default_h), pygame.RESIZABLE | pygame.DOUBLEBUF
            )
            self.width, self.height = default_w, default_h
        else:  # Go fullscreen
            try:
                info = pygame.display.Info()
                self.width = info.current_w
                self.height = info.current_h
                self.screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF
                )
            except pygame.error:
                self.width, self.height = 1920, 1080
                self.screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF
                )
        pygame.display.set_caption(current_caption)
        self.fullscreen = not self.fullscreen
        self.bar_area_height = self.height - 70
        try:
            self.font = pygame.font.SysFont("Consolas", 24)
            self.title_font = pygame.font.SysFont("Consolas", 36, bold=True)
        except Exception as e:
            print(f"Warning: Font reloading error ({e}). Using Arial.")
            self.font = pygame.font.SysFont("Arial", 24)
            self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self._draw_frame()  # Redraw after mode change

    def _draw_info_text(self, end, final_screen=False):  # Add final_screen flag
        """Draw the algorithm title and other info text, adapting for final screen."""
        # --- Draw Algorithm Title (Top Center) ---
        try:
            title_surface = self.title_font.render(
                self.algorithm_name, True, self.title_color
            )
            title_rect = title_surface.get_rect(center=(self.width // 2, 25))
            self.screen.blit(title_surface, title_rect)
            info_y_pos = title_rect.top + 5  # Start below the title
        except Exception as e:
            print(f"Error rendering title font: {e}")
            info_y_pos = 15  # Fallback position

        # --- Draw Other Info (Below Title) ---
        try:
            # Determine Timer Text
            timer_prefix = "Final Time:" if final_screen else "Time:"
            # Update elapsed time only if running and not paused/final
            if not end and not self.paused and not final_screen:
                self.elapsed_time = time.time() - self.start_time
            timer_text_surface = self.font.render(
                f"{timer_prefix} {self.elapsed_time:.2f}s", True, self.text_color
            )

            # Blit Timer
            self.screen.blit(timer_text_surface, (10, info_y_pos))

            # Determine and Blit Control Hints based on state
            if final_screen:
                # Only show Quit/Restart on final screen
                controls_text_surface = self.font.render(
                    "Quit [Q] Restart [R]", True, self.text_color
                )
                self.screen.blit(
                    controls_text_surface,
                    (self.width - controls_text_surface.get_width() - 10, info_y_pos),
                )
            else:
                # Show standard controls during sorting
                current_x = (
                    10 + timer_text_surface.get_width() + 30
                )  # Position relative to timer

                delay_text_surface = self.font.render(
                    f"Delay: {self.delay_ms}ms [+/-]", True, self.text_color
                )
                self.screen.blit(delay_text_surface, (current_x, info_y_pos))
                current_x += delay_text_surface.get_width() + 30

                pause_text_str = "PAUSED [P]" if self.paused else "Running [P]"
                pause_restart_surface = self.font.render(
                    f"{pause_text_str} Restart [R]", True, self.text_color
                )
                self.screen.blit(pause_restart_surface, (current_x, info_y_pos))

                quit_fullscreen_surface = self.font.render(
                    "Quit [Q] Fullscreen [ESC]", True, self.text_color
                )
                self.screen.blit(
                    quit_fullscreen_surface,
                    (self.width - quit_fullscreen_surface.get_width() - 10, info_y_pos),
                )

        except Exception as e:
            print(f"Error rendering info font: {e}")

    def _draw_frame(
        self,
        highlight_indices=[],
        moving_index=None,
        end=False,
        sweep=False,
        final_screen=False,
    ):  # Add final_screen param
        """Draws a single frame of the visualization."""
        try:
            self.screen.fill(self.bg_color)  # Clear screen first
        except Exception as e:
            print(f"Error filling screen: {e}")
            return  # Avoid drawing if screen fill fails

        bar_total_width = self.width / self.n if self.n > 0 else self.width
        bar_spacing = max(0, int(bar_total_width * 0.1))
        bar_render_width = max(1, math.ceil(bar_total_width - bar_spacing))

        # Draw Bars
        for i, val in enumerate(self.array):
            x = int(i * bar_total_width)
            bar_height = max(
                0,
                (
                    (val / self.max_value) * self.bar_area_height
                    if self.max_value > 0
                    else 0
                ),
            )
            y = self.height - bar_height
            color = self._get_bar_color(i, val, highlight_indices, moving_index, sweep)
            try:
                pygame.draw.rect(
                    self.screen, color, (x, y, bar_render_width, bar_height)
                )
            except Exception as e:
                print(
                    f"Error drawing rect at ({x},{y}) size ({bar_render_width},{bar_height}): {e}"
                )

        # Draw Info Text (passing the flag)
        self._draw_info_text(end, final_screen)  # Pass final_screen flag here

        # Update Display
        try:
            pygame.display.flip()
        except Exception as e:
            print(f"Error flipping display: {e}")

    def _handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_ESCAPE:
                    try:
                        self.toggle_fullscreen()
                    except Exception as e:
                        print(f"Error toggling fullscreen: {e}")
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    caption_suffix = " [PAUSED]" if self.paused else ""
                    try:
                        pygame.display.set_caption(
                            f"Sorting Visualizer - {self.algorithm_name}{caption_suffix}"
                        )
                    except Exception as e:
                        print(f"Error setting caption: {e}")
                elif event.key == pygame.K_r:
                    print("Restart requested...")
                    self.restart_requested = True
                elif (
                    event.key == pygame.K_PLUS
                    or event.key == pygame.K_KP_PLUS
                    or event.key == pygame.K_EQUALS
                ):
                    self.delay_ms = min(
                        self.max_delay,
                        self.delay_ms + 1 if self.delay_ms < 10 else self.delay_ms + 5,
                    )
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.delay_ms = max(
                        self.min_delay,
                        self.delay_ms - 1 if self.delay_ms <= 10 else self.delay_ms - 5,
                    )
            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                try:
                    if event.w > 0 and event.h > 0:  # Ensure valid dimensions
                        self.width, self.height = event.w, event.h
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height),
                            pygame.RESIZABLE | pygame.DOUBLEBUF,
                        )
                        self.bar_area_height = self.height - 70
                        self._draw_frame()  # Redraw immediately
                except Exception as e:
                    print(f"Error handling resize event: {e}")

    def reset_timer(self):
        self.start_time = time.time()
        self.elapsed_time = 0

    def reset_array(self):
        self.array = list(self.original_array)
        self.n = len(self.array)
        self.max_value = max(self.array) if self.array else 1
        self._draw_frame()  # Redraw immediately to show reset state
        pygame.time.delay(50)

    def update(
        self, array, highlight_indices=[], moving_index=None, end=False, sweep=False
    ):
        if not self.running:
            return
        self._handle_events()
        if not self.running:
            return  # Check again after handling events
        if self.restart_requested:
            self.restart_requested = False
            raise RestartAlgorithm()
        while self.paused and self.running:
            self._draw_frame(
                highlight_indices, moving_index, end, sweep
            )  # Draw paused state
            self._handle_events()
            if not self.running:
                return
            if self.restart_requested:
                self.restart_requested = False
                raise RestartAlgorithm()
            pygame.time.delay(100)  # Yield CPU while paused
        # Normal Update
        self.array = list(array)
        # Calls _draw_frame with default final_screen=False
        self._draw_frame(highlight_indices, moving_index, end, sweep)
        # Sound logic
        sound_value = None
        if moving_index is not None and 0 <= moving_index < len(self.array):
            sound_value = self.array[moving_index]
        if sound_value is not None:
            self.sound_manager.play_sound(sound_value)
        # Delay
        if self.delay_ms > 0:
            pygame.time.delay(self.delay_ms)

    def finalize(self):
        """Keeps the final sorted state displayed until user action."""
        if not self.running:
            return  # Don't enter finalize loop if already stopped

        self.running = True  # Ensure loop runs if we got here

        # Draw the final frame using _draw_frame with the new flag
        # This now handles drawing bars and the correct final info text
        self._draw_frame(end=True, final_screen=True)

        while self.running:
            self._handle_events()  # Still handle events (Quit, R, ESC)
            if not self.running:
                break  # Exit if Q pressed or window closed
            # Check for restart request from the final screen
            if self.restart_requested:
                self.restart_requested = False
                raise RestartAlgorithm()  # Signal main loop to restart
            pygame.time.delay(100)  # Prevent high CPU usage
