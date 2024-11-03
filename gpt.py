import tkinter as tk
import pyautogui
import win32gui
import win32con
import threading
import time
import random
import keyboard
import webbrowser

def start_timer():
    print("Starting timer window...")  # Debug
    root = tk.Tk()
    root.geometry("200x100")
    tk.Label(root, text="Pick a timer duration:").pack()
    
    for minutes in [1, 3, 5]:
        tk.Button(root, text=f"{minutes} min", command=lambda m=minutes: run_annoyance(m)).pack()
    
    root.mainloop()

def run_annoyance(minutes):
    duration = minutes * 60
    print(f"Annoyance timer set for {minutes} minutes.")  # Debug
    timer_thread = threading.Thread(target=annoy_user, args=(duration,))
    timer_thread.start()
    
    # Start a separate thread for panic mode detection
    panic_thread = threading.Thread(target=detect_panic_mode)
    panic_thread.start()

def detect_panic_mode():
    # Monitor for Alt+F4
    while True:
        if keyboard.is_pressed("alt+f4"):
            print("Panic mode activated!")  # Debug
            panic_mode()
            time.sleep(1)  # Avoid rapid re-triggering

def panic_mode():
    # Get all open window handles and move each to a random position
    def enum_windows(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            try:
                rect = win32gui.GetWindowRect(hwnd)
                window_x, window_y, window_width, window_height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
                
                # Move window to a random position on the screen
                screen_width, screen_height = pyautogui.size()
                new_x = random.randint(0, screen_width - window_width)
                new_y = random.randint(0, screen_height - window_height)
                
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, window_width, window_height, 0)
                print(f"Window scattered to: ({new_x}, {new_y})")  # Debug
            except:
                pass

    # Enumerate through all windows and apply the scatter effect
    win32gui.EnumWindows(enum_windows, None)

def annoy_user(duration):
    end_time = time.time() + duration
    print("Annoyance started...")  # Debug
    while time.time() < end_time:
        move_away_from_close_button()
        time.sleep(0.001)  # Reduced from 0.02 to 0.001 for faster updates
    finish_annoying()

def move_away_from_close_button():
    # Get handle of all visible windows
    def enum_windows(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            # Move the close button for each window
            window_x, window_y, window_width, window_height = get_window_rect(hwnd)
            close_button_x = window_x + window_width - 10
            close_button_y = window_y + 10
            mouse_x, mouse_y = pyautogui.position()
            if is_mouse_near_close_button(mouse_x, mouse_y, close_button_x, close_button_y):
                dodge_window(hwnd, window_x, window_y, window_width, window_height)

    win32gui.EnumWindows(enum_windows, None)

def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

def dodge_window(hwnd, window_x, window_y, window_width, window_height):
    screen_width, screen_height = pyautogui.size()
    new_x = max(0, min(window_x + random.choice([-30, 30]), screen_width - window_width))
    new_y = max(0, min(window_y + random.choice([-30, 30]), screen_height - window_height))
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, window_width, window_height, 0)
    print(f"Window dodged to: ({new_x}, {new_y})")  # Debug

def is_mouse_near_close_button(mouse_x, mouse_y, close_button_x, close_button_y):
    return abs(mouse_x - close_button_x) < 150 and abs(mouse_y - close_button_y) < 150  # Increased from 40 to 150

def finish_annoying():
    print("Annoyance finished!")  # Debug
    show_close_image_dialog()

def show_close_image_dialog():
    close_dialog = tk.Toplevel()
    close_dialog.geometry("300x200")
    close_dialog.title("Close")
    
    close_img = tk.PhotoImage(file="close_button_image.png")
    close_label = tk.Label(close_dialog, image=close_img)
    close_label.image = close_img  # Keep a reference to avoid garbage collection
    close_label.pack()
    close_label.bind("<Button-1>", lambda e: open_youtube_video())
    tk.Label(close_dialog, text="Click the 'Close' image!").pack()

def open_youtube_video():
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(video_url)
    print("YouTube video opened!")  # Debug

# Start the prank
start_timer()
