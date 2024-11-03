import tkinter as tk
import pyautogui
import win32gui
import win32con
import threading
import time
import random
import keyboard  # For detecting Alt+F4
from PIL import Image, ImageTk
import webbrowser
import os

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
        time.sleep(0.001)  # Reduced from 0.01 to 0.001 for better responsiveness
    finish_annoying()

def move_away_from_close_button():
    mouse_x, mouse_y = pyautogui.position()
    
    def check_window(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            try:
                rect = win32gui.GetWindowRect(hwnd)
                window_x, window_y, window_width, window_height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
                
                # Calculate close button area (top-right corner) - increased detection area
                close_button_x = window_x + window_width - 100  # Increased from 65 to 100
                close_button_y = window_y + 40  # Increased from 25 to 40

                if is_mouse_near_close_button(mouse_x, mouse_y, close_button_x, close_button_y):
                    # Check if window is maximized and restore if it is
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    if style & win32con.WS_MAXIMIZE:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        rect = win32gui.GetWindowRect(hwnd)
                        window_x, window_y, window_width, window_height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

                    screen_width, screen_height = pyautogui.size()
                    
                    # Determine which side of the screen the window is on and jump to opposite side
                    if window_x < screen_width / 2:
                        new_x = screen_width - window_width - 50  # Jump to right side
                    else:
                        new_x = 50  # Jump to left side
                        
                    if window_y < screen_height / 2:
                        new_y = screen_height - window_height - 50  # Jump to bottom
                    else:
                        new_y = 50  # Jump to top
                    
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, 
                                        window_width, window_height, 
                                        win32con.SWP_SHOWWINDOW)
                    return
            except:
                pass

    win32gui.EnumWindows(check_window, None)

def is_mouse_near_close_button(mouse_x, mouse_y, close_button_x, close_button_y):
    # Increased detection area
    return abs(mouse_x - close_button_x) < 100 and abs(mouse_y - close_button_y) < 100  # Increased from 60 to 100
def finish_annoying():
    print("Annoyance finished!")  # Debug
    
    # Create a Tkinter window for custom dialog
    dialog = tk.Tk()
    dialog.title("Congratulations!")
    
    # Load and display the trollface image
    try:
        # Get the absolute path to the image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "trollface.jpg")
        print(f"Attempting to load image from: {image_path}")  # Debug
        
        # Load JPG image using PIL
        pil_image = Image.open(image_path)
        # Optionally resize the image if it's too large
        pil_image = pil_image.resize((200, 200))  # Adjust size as needed
        photo = ImageTk.PhotoImage(pil_image)
        img_label = tk.Label(dialog, image=photo)
        img_label.photo = photo  # Keep a reference!
        img_label.pack(pady=10)
        print(f"Image size: {pil_image.size}")  # Add this after pil_image = Image.open(image_path)
    except Exception as e:
        print(f"Image loading error: {e}")  # Debug
        # Fallback if image fails to load
        tk.Label(dialog, text="😈", font=("Arial", 48)).pack(pady=10)
    
    tk.Label(dialog, text="Congrats! You can close windows now!").pack(pady=10)
    
    def on_ok():
        # Create a separate thread for opening the browser
        threading.Thread(target=lambda: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")).start()
        dialog.destroy()
    
    tk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
    
    # Center the dialog on screen
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make sure the dialog stays on top
    dialog.attributes('-topmost', True)
    dialog.mainloop()
    dialog.attributes('-topmost', True)
    dialog.mainloop()

# Start the prank
start_timer()
start_timer()