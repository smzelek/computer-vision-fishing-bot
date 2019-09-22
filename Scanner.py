from PIL import ImageGrab
import Controller

class Scanner():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.water_values = {}
        print(self.end)
        print(self.start)

    def scan_water(self):
        y = self.start[1]
        while y < self.end[1]:
            x = self.start[0]
            while (x < self.end[0]):
                Controller.set_mouse_pos([x, y])
                check = grab_avg([x,y])
                self.waterVals[(x,y)] = check
                x = x + 20
            y = ycount + 10

    # def findBobber():
    #     ycount = ystart
    #     while ycount < yend:
    #         xcount = xstart
    #         while (xcount < xend) and (time.time() < globaltime + 25):
    #             set_mouse_pos([xcount, ycount])
    #             time.sleep(.001)
    #             val_at_check = grab_avg([xcount, ycount])
    #             rgbdiff = rgb_distance(val_at_check, bobberVal)
    #             if rgbdiff < int(bobberSensitivity.get()):
    #                 set_mouse_pos((xcount,ycount))
    #                 time.sleep(.3)
    #                 print "Bobber found"
    #                 return True
    
    #             xcount = xcount + 20
    #         ycount = ycount + 10
    #     return False

def grab_img(pos): 
     box = (pos[0] - 5, pos[1] - 5, pos[0] + 5, pos[1] + 5)
     return ImageGrab.grab(box)

def grab_avg(pos):
    im = grab_img(pos).convert('RGB')
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
