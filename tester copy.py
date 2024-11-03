import win32gui
import win32con
import pyautogui
import time
import random
import threading
import webbrowser
import os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG, QObject, pyqtSignal

class SignalHandler(QObject):
    finished = pyqtSignal()

signal_handler = SignalHandler()

def move_away_from_close_button():
    mouse_x, mouse_y = pyautogui.position()
    
    def check_window(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            try:
                rect = win32gui.GetWindowRect(hwnd)
                window_x, window_y, window_width, window_height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
                
                # Calculate close button area (top-right corner)
                close_button_x = window_x + window_width - 150
                close_button_y = window_y + 80

                if abs(mouse_x - close_button_x) < 150 and abs(mouse_y - close_button_y) < 150:
                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    if style & win32con.WS_MAXIMIZE:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        rect = win32gui.GetWindowRect(hwnd)
                        window_x, window_y, window_width, window_height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

                    new_x = window_x + random.randint(-200, 200)
                    new_y = window_y + random.randint(-200, 200)
                    
                    screen_width, screen_height = pyautogui.size()
                    new_x = max(0, min(new_x, screen_width - window_width))
                    new_y = max(0, min(new_y, screen_height - window_height))
                    
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, 
                                        window_width, window_height, 0)
                    return
            except:
                pass

    win32gui.EnumWindows(check_window, None)

def annoy_user(duration):
    end_time = time.time() + duration
    print("Annoyance started...")
    
    pyautogui.FAILSAFE = False
    
    while time.time() < end_time:
        move_away_from_close_button()
        time.sleep(0.001)
    
    print("Timer finished, showing final dialog...")
    signal_handler.finished.emit()

def finish_annoying():
    print("Annoyance finished!")
    
    dialog = QDialog()
    dialog.setWindowTitle("U didnt get it huh!")
    dialog.setFixedSize(300, 400)
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    
    layout = QVBoxLayout()
    
    try:
        image_path = "trollface.png"
        print(f"Attempting to load image from: {image_path}")
        
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignCenter)
        
    except Exception as e:
        print(f"Image loading error: {e}")
        emoji_label = QLabel("😈")
        emoji_label.setFont(QFont("Arial", 48))
        layout.addWidget(emoji_label, alignment=Qt.AlignCenter)
    
    text_label = QLabel("BRUHHHHH!!!")
    text_label.setFont(QFont("Arial", 12, QFont.Bold))
    layout.addWidget(text_label, alignment=Qt.AlignCenter)
    
    def on_ok():
        # Create a separate thread for opening the browser
        threading.Thread(target=lambda: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")).start()
        dialog.close()
    
    ok_button = QPushButton("Quit")
    ok_button.setFont(QFont("Arial", 10))
    ok_button.setFixedWidth(100)
    ok_button.clicked.connect(on_ok)
    layout.addWidget(ok_button, alignment=Qt.AlignCenter)
    
    dialog.setLayout(layout)
    
    # Center the dialog
    screen = QApplication.primaryScreen().geometry()
    x = (screen.width() - dialog.width()) // 2
    y = (screen.height() - dialog.height()) // 2
    dialog.move(x, y)
    
    dialog.exec_()

def run_annoyance(minutes):
    duration = minutes * 60
    # Create and start the thread
    thread = threading.Thread(target=lambda: annoy_user(duration))
    thread.daemon = True
    signal_handler.finished.connect(finish_annoying)
    thread.start()

def start_timer():
    print("Starting timer window...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = QDialog()
    dialog.setWindowTitle("Timer Selection")
    dialog.setFixedSize(200, 150)
    
    layout = QVBoxLayout()
    
    label = QLabel("Pick a timer duration:")
    label.setFont(QFont("Arial", 10))
    layout.addWidget(label, alignment=Qt.AlignCenter)
    
    for minutes in [1, 3, 5]:
        button = QPushButton(f"{minutes} min")
        button.clicked.connect(lambda checked, m=minutes: (dialog.close(), run_annoyance(m)))
        layout.addWidget(button)
    
    dialog.setLayout(layout)
    
    screen = QApplication.primaryScreen().geometry()
    x = (screen.width() - dialog.width()) // 2
    y = (screen.height() - dialog.height()) // 2
    dialog.move(x, y)
    
    dialog.exec_()

def open_url(url):
    """Try multiple methods to open URL"""
    methods = [
        lambda: webbrowser.open_new(url),
        lambda: os.system(f'start {url}'),
        lambda: os.startfile(url),
        lambda: webbrowser.get('windows-default').open(url)
    ]
    
    for method in methods:
        try:
            method()
            return True
        except:
            continue
    return False

if __name__ == '__main__':
    app = QApplication([])
    start_timer()
    app.exec_()