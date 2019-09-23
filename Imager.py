from PIL import ImageGrab
from numpy import array

def grab_img(pos): 
    box = (pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10)
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
