import time
from pynput import keyboard, mouse

start_time = None
terminate_program = False


def on_key_press(key):
    global start_time, terminate_program
    if key == keyboard.Key.esc:
        # Signal to terminate the program
        terminate_program = True
        return False  # Stop the keyboard listener
    end_time = time.time()
    lag = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Keyboard input lag for key {key}: {lag:.2f} ms")


def on_click(x, y, button, pressed):
    global start_time
    if pressed:  # Measure on mouse press
        end_time = time.time()
        lag = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Mouse click lag for {button}: {lag:.2f} ms")
    # Check if the program should terminate after a mouse event
    if terminate_program:
        return False  # Stop the mouse listener


def main():
    global start_time, terminate_program
    print("Press any key or mouse button to measure input lag. Press ESC to exit.")

    # Start the keyboard listener in a non-blocking fashion
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()

    # Start the mouse listener in a non-blocking fashion
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    try:
        while not terminate_program:
            start_time = time.time()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        keyboard_listener.stop()
        mouse_listener.stop()
        keyboard_listener.join()
        mouse_listener.join()
        print("Exiting application...")


if __name__ == "__main__":
    main()
