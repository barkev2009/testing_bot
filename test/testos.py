import win32gui
import re
import win32con
import os

class WindowFinder:
    """Class to find and make focus on a particular Native OS dialog/Window """
    def __init__ (self):
        self._handle = None

    def find_window(self, class_name, window_name = None):
        """Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """Get the focus on the desired open window"""
        win32gui.SetForegroundWindow(self._handle)
    
    def click_button(self):
        def print_some(hwnd, wildcard):
            if win32gui.GetClassName(hwnd) == 'Button' and 'Открыть' in win32gui.GetWindowText(hwnd):
                # Нажатие на объект
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
            print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumChildWindows(self._handle, print_some, None)
        # button = win32gui.FindWindowEx(self._handle, None,'Button', None) 
        # # Press the left mouse button
        # win32gui.SendMessage(button, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        # # Left mouse button up
        # win32gui.SendMessage(button, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    
    def input_path(self, path_name):
        def print_some(hwnd, wildcard):
            if win32gui.GetClassName(hwnd) == 'Edit':
                # Фокусирование на объекте
                win32gui.SetForegroundWindow(hwnd)

                # Нажатие на объект
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

                # Печать текста
                win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, path_name)
            # print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumChildWindows(self._handle, print_some, None)

win = WindowFinder()
win.find_window_wildcard(".*Открытие*") 
win.set_foreground()
path = ['C:\\', 'Users', 'barke', 'Downloads', 'spark.docx']
win.input_path(os.path.join(*path))
win.click_button()