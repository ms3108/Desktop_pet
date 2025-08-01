import platform

if platform.system() == "Windows":
    import win32api
    import win32con
    import win32gui


def is_fullscreen():
    if platform.system() != "Windows":
        return False

    hwnd = win32gui.GetForegroundWindow()
    rect = win32gui.GetWindowRect(hwnd)

    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    x1, y1, x2, y2 = rect
    window_width = x2 - x1
    window_height = y2 - y1

    return window_width == screen_width and window_height == screen_height
