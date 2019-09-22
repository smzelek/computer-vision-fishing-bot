import win32api, win32con
import win32com.client
import autopy
import threading
import time

def set_mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x
    y = y
    return (x,y)

def cast():
    autopy.key.tap("1")
    time.sleep(1)

def loot():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(.2)
    
def use_bauble():
    autopy.key.tap("2")
    time.sleep(7)

def wait_for_click():
    waitformouse = threading.Thread(target=__await_click)
    waitformouse.start()
    waitformouse.join()

def __await_click():
    state_left = win32api.GetKeyState(0x01) 
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:
            state_left = a
            if not a < 0:
                return
        time.sleep(0.001)