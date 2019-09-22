from PIL import ImageTk, Image, ImageGrab, ImageOps
import Tkinter 
import os
import win32api, win32con
import time
from threading import Thread
import win32com.client
import autopy
import sys 


#screenshot: https://imgur.com/WN65CG3

#packages needed:
#   numpy: http://www.numpy.org/
#   PIL: http://www.pythonware.com/products/pil/
#   pywin: http://sourceforge.net/projects/pywin32/
#   autopy: https://pypi.python.org/pypi/autopy/
#
# installation of these packages may be the hardest part.


# Globals
# ------------------

shell = win32com.client.Dispatch("WScript.Shell")

globaltime = 0
reelcount = 0

xstart = 0
xend = 0
ystart = 0
yend = 0

mainwindow = Tkinter.Tk()
targetStartText = Tkinter.StringVar()
targetEndText = Tkinter.StringVar()
waterText = Tkinter.StringVar()
bobberText = Tkinter.StringVar()
differenceText = Tkinter.StringVar()

fishingLengthInput = Tkinter.StringVar()
fishingLengthInput.set("0")

bobberVal = [0,0,0]
waterVal = [0,0,0]
diffVal = 0
baubleflag = Tkinter.IntVar()

bobberImg = None
avgWaterImg = None
bobberSensitivity = Tkinter.StringVar()
bobberSensitivity.set("300")

waterVals = {}

#---------------------------------

def set_mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x
    y = y
    return (x,y)

def grab_img(mousepos): 
     box = (mousepos[0] - 5, mousepos[1] - 5, mousepos[0] + 5, mousepos[1] + 5)
     return ImageGrab.grab(box)

def grab_avg(mousepos):
    im = grab_img(mousepos).convert('RGB')
    a = array(im.getdata())
    reds = [pair[0] for pair in a]
    greens = [pair[1] for pair in a]
    blues = [pair[2] for pair in a]
    r = sum(reds)/len(reds)
    g = sum(greens)/len(greens)
    b = sum(blues)/len(blues)
    return [r, g, b]

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

def rgb_distance(rgb1, rgb2):
    dred = rgb1[0] - rgb2[0]
    dgreen = rgb1[1] - rgb2[1]
    dblue = rgb1[2] - rgb2[2]
    
    return dred*dred + dgreen*dgreen + dblue*dblue

def cast():
    autopy.key.tap("1")
    time.sleep(1)

def scan_water(canvas, element):
    global xstart, ystart, xend, yend, waterVal, bobberVal, diffVal

    ycount = ystart
    while ycount < yend:
        xcount = xstart
        while (xcount < xend):
            set_mouse_pos([xcount, ycount])
            check = grab_avg([xcount,ycount])
            waterVals[(xcount,ycount)] = check
            xcount = xcount + 20
        ycount = ycount + 10
    waterVal = [waterVals[0]/numChecks, waterVals[1]/numChecks, waterVals[2]/numChecks]
    hexcolor = rgb_to_hex(waterVal)
    canvas.itemconfig(element, fill=hexcolor) # change color

    if bobberVal and waterVal:
        diffVal = rgb_distance(bobberVal, waterVal)
        differenceText.set(diffVal)

    waterText.set(waterVal)

def findBobber():
    global globaltime, xstart, ystart, xend, yend, bobberVal, diffVal
    ycount = ystart

    while ycount < yend:
        xcount = xstart
        while (xcount < xend) and (time.time() < globaltime + 25):
            set_mouse_pos([xcount, ycount])
            time.sleep(.001)
            val_at_check = grab_avg([xcount, ycount])
            rgbdiff = rgb_distance(val_at_check, bobberVal)
            if rgbdiff < int(bobberSensitivity.get()):
                set_mouse_pos((xcount,ycount))
                time.sleep(.3)
                print "Bobber found"
                return True
 
            xcount = xcount + 20
        ycount = ycount + 10
    return False

def loot():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(.2)

def reelIn():
    global globaltime
    mousePos = get_cords()
    idle_bobber = grab_avg(mousePos)
    
    splashSensitivity = 400

    while (time.time() < globaltime + 25):
        current_bobber = grab_avg(mousePos)
        diff = rgb_distance(idle_bobber, current_bobber)
        if diff > splashSensitivity:
            print "Reeled in a big one!"
            global reelcount
            reelcount = reelcount + 1
            loot()
            break
    
def use_bauble():
    autopy.key.tap("2")
    time.sleep(7)

def create_setup_GUI():
    mainwindow.title(';)') 
    mainwindow.wm_attributes("-topmost", 1)
    mainwindow.protocol("WM_DELETE_WINDOW", sys.exit)

    Tkinter.Label(mainwindow, text="Target Start", anchor="e").grid(row=0)
    Tkinter.Label(mainwindow, textvariable=targetStartText, anchor="w").grid(row=0, column=1)
    
    Tkinter.Label(mainwindow, text="Target End").grid(row=1)
    Tkinter.Label(mainwindow, textvariable=targetEndText).grid(row=1, column=1)
    
    # Tkinter.Label(mainwindow, text="Water Value").grid(row=2)
    # Tkinter.Label(mainwindow, textvariable=waterText).grid(row=2, column=1)
    
    # water variance PER square
    # sensitivity can therefore be per square



    # Tkinter.Label(mainwindow, text="Bobber Value").grid(row=3)
    # Tkinter.Label(mainwindow, textvariable=bobberText).grid(row=3, column=1)

    # Tkinter.Label(mainwindow, text="Difference").grid(row=4)
    # Tkinter.Label(mainwindow, textvariable=differenceText).grid(row=4, column=1)

    # Tkinter.Label(mainwindow, text="Water Color").grid(row=5)
    # watercanvas = Tkinter.Canvas(mainwindow, width=20, height=20)
    # waterColorElement = watercanvas.create_rectangle(0, 0, 20, 20, fill="black")
    # watercanvas.grid(row=5, column=1)

    # Tkinter.Label(mainwindow, text="Bobber Color:").grid(row=6)
    # bobberColorCanvas = Tkinter.Canvas(mainwindow, width=20, height=20)
    # bobberColorElement = bobberColorCanvas.create_rectangle(0, 0, 20, 20, fill="black")
    # bobberColorCanvas.grid(row=6, column=1)

    # bobberImageCanvas = Tkinter.Canvas(mainwindow, width=20, height=20, relief="solid")
    # bobberImageCanvas.grid(row=6, column=2)

    # Tkinter.Label(mainwindow, text='Bobber Sensitivity').grid(row=7, column=0)
    # Tkinter.Entry(mainwindow, textvariable=bobberSensitivity, width=10).grid(row=7, column=1)

    Tkinter.Label(mainwindow, text='Fish For Minutes').grid(row=8, column=0)
    Tkinter.Entry(mainwindow, textvariable=fishingLengthInput, width=10).grid(row=8, column=1)

    Tkinter.Label(mainwindow, text='Use Bauble?').grid(row=9, column=0)
    Tkinter.Checkbutton(mainwindow, text="", variable=baubleflag).grid(row=9, column=1)
    
    Tkinter.Button(mainwindow, text='Set Mouse Start', width=25, command=set_mouse_start).grid(row=10, columnspan=3)
    Tkinter.Button(mainwindow, text='Set Mouse End', width=25, command=set_mouse_end).grid(row=11, columnspan=3)
    
    # Tkinter.Button(mainwindow, text='Check Bobber', width=25, command= lambda: check_bobber(bobberColorCanvas, bobberColorElement, bobberImageCanvas)).grid(row=12, columnspan=3)
    
    Tkinter.Button(mainwindow, text='Scan Water', width=25, command= lambda: scan_water(watercanvas, waterColorElement)).grid(row=13, columnspan=3)

    Tkinter.Button(mainwindow, text='Go', width=25, command=mainwindow.destroy).grid(row=14, columnspan=3)

    mainwindow.mainloop() 

def create_fishing_GUI():
    return

def wait_for_click():
    state_left = win32api.GetKeyState(0x01) 
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:
            state_left = a
            if not a < 0:
                return
        time.sleep(0.001)

def check_bobber(canvas, element, bobberImgCanvas): 
    global bobberVal, waterVal, diffVal, bobberImg

    waitformouse = Thread(target=wait_for_click)
    waitformouse.start()
    waitformouse.join()

    time.sleep(0.3)

    mouseloc = get_cords()
    rgb = grab_avg(mouseloc)
    hexcolor = rgb_to_hex(rgb)
    canvas.itemconfig(element, fill=hexcolor) # change color

    bobberImg = ImageTk.PhotoImage(grab_img(mouseloc).resize((20,20),Image.NEAREST))
    bobberImgCanvas.create_image(0, 0, anchor="nw", image=bobberImg)

    bobberVal = rgb

    if bobberVal and waterVal:
        diffVal = rgb_distance(bobberVal, waterVal)
        differenceText.set(diffVal)

    bobberText.set(bobberVal)

def set_mouse_start():
    global xstart, ystart 
    waitformouse = Thread(target=wait_for_click)
    waitformouse.start()
    waitformouse.join()

    time.sleep(0.01)

    start = get_cords()
    xstart = start[0]
    ystart = start[1]

    targetStartText.set('({}, {})'.format(xstart, ystart))
    
def set_mouse_end():
    global xend, yend
    waitformouse = Thread(target=wait_for_click)
    waitformouse.start()
    waitformouse.join()

    time.sleep(0.01)

    end = get_cords()
    xend = end[0]
    yend = end[1]
    
    targetEndText.set('({}, {})'.format(xend, yend))

def main():
    global xstart,ystart,xend,yend,reelcount,globaltime,bobberVal,baubleflag
    
    create_setup_GUI()
    
    runtime = int(fishingLengthInput.get())
    reelcount = 0
    flag = False

    if runtime == 0:
        print "Running infinitely."
        flag = True

    time.sleep(.1)
    set_mouse_pos([xstart, ystart])

    if baubleflag == 1:
        use_bauble()
        lastused = time.time()

    starttime = time.time()
    while (flag or time.time() < runtime * 60 + starttime):
        
        if baubleflag == 1 and ((time.time() - lastused)/60 > 10):
            use_bauble()
            lastused = time.time()
            
        cast()
        
        globaltime = time.time()
        time.sleep(1)
        if findBobber():
            reelIn()
            elapsedMins = int((time.time() - starttime)/60)
            print "" + str(reelcount) + " reels in " + str(elapsedMins) + " mins."
        time.sleep(4)
    print "Fishing completed."
    
    
if __name__ == '__main__':
    main()
