import win32gui
import re
import win32con
import os
from datetime import datetime
import uuid
import traceback

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def dotify(dictionary: dict):
    dictionary = dotdict(dictionary)
    for k, v in dictionary.items():
        if type(v) == dict:
            dictionary[k] = dotify(v)
    return dictionary


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        win32gui.EnumChildWindows(self._handle, print_some, None)
    
    def input_path(self, path_name):
        rects = []
        def print_some(hwnd, wildcard):
            if win32gui.GetClassName(hwnd) == 'Edit':
                # Фокусирование на объекте
                win32gui.SetForegroundWindow(hwnd)

                # Нажатие на объект
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

                # Печать текста
                win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, path_name)
            rects.append(win32gui.GetWindowRect(hwnd))
        win32gui.EnumChildWindows(self._handle, print_some, None)
    

def exit_with_grace(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            counter += 1
            print(f'{bcolors.FAIL}Попыток израсходовано: {counter} | Функция: {func.__name__} | Ошибка: {bcolors.OKBLUE}{repr(e)}{bcolors.ENDC}')
            traceback_uuid = str(uuid.uuid4())
            print(f'{bcolors.FAIL}Traceback ID: {bcolors.OKBLUE}{traceback_uuid}{bcolors.ENDC}')
            with open(os.path.join('logs', f'{datetime.now().strftime("%d.%m.%Y")}.log'), 'a', encoding='utf-8') as file:
                file.write(f'Traceback ID: {traceback_uuid}\n')
                file.write(traceback.format_exc())
                file.write('\n'*5)
    return wrapper