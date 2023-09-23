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

# import win32api, win32gui, win32con

# # find the parent window (eg. dialog box),
# # replace the last two parameters to match the appropriate window
# hwnd = win32gui.FindWindowEx(0, 0, 0, "Сохранение")
# print(hwnd)
# print(win32gui.GetWindowText(hwnd))

# # find the OK button
# hbutton = win32gui.FindWindowEx(hwnd, None, None, None)
# print(hbutton)
# print(win32gui.GetWindowText(hbutton))

# # mouse button click on the OK button, WM_COMMAND may work too
# win32api.PostMessage(hbutton, win32con.WM_LBUTTONDOWN, 0, 0)
# win32api.PostMessage(hbutton, win32con.WM_LBUTTONUP, 0, 0)

# def callback(hwnd, extra):
#     if win32gui.IsWindowVisible(hwnd):
#         print(f"window text: '{win32gui.GetWindowText(hwnd)}'")

# win32gui.EnumWindows(callback, None)

# from datetime import datetime, timedelta
# print((datetime.now() + timedelta(days=30)).strftime("%d.%m.%Y"))