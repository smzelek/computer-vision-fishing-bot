import sys
import win32api, win32con
import win32com.client
import threading
import ctypes
from ctypes import wintypes
byref = ctypes.byref
user32 = ctypes.windll.user32

class PauseListener():
    def __init__(self, callback):
        self.callback = callback
        self.wait_for_pause()

    def wait_for_pause(self):
        waitforpause = threading.Thread(target=lambda:self.__await_pause())
        waitforpause.daemon = True
        waitforpause.start()
        return waitforpause
        
    def __await_pause(self):
        user32.RegisterHotKey (None, 1, None, win32con.VK_F3)
        msg = wintypes.MSG ()
        while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                self.callback()
        
