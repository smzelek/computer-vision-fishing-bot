import Imager
from collections import OrderedDict
import time

class Scanner():
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.water_values = OrderedDict()
        self.find_start_time = 0
        self.bobber_cords = None

        self.original_water_rgb = [0,0,0]
        self.scanning_water_rgb = [0,0,0]
        self.last_5_diffs = []
        self.water_sensitivity = 300
        self.bobber_sensitivity = 300

        self.scan_water()
        
    def scan_water(self):
        y = self.start[1]
        while y < self.end[1]:
            x = self.start[0]
            while (x < self.end[0]):
                check = Imager.grab_avg([x,y])
                self.water_values[(x,y)] = check
                x = x + 20
            y = y + 10

    def find_bobber(self):
        self.find_start_time = time.time()
        self.last_5_diffs = []

        for key, value in self.water_values.items():
            if time.time() > self.find_start_time + 25:
                return False

            scan_value = Imager.grab_avg(key)
            rgb_diff = Imager.rgb_distance(scan_value, value)
            
            self.original_water_rgb = value
            self.scanning_water_rgb = scan_value    
            self.add_diff(rgb_diff)

            if rgb_diff > self.water_sensitivity:
                self.bobber_cords = key
                return True
        return False

    def wait_for_splash(self):
        idle_bobber = Imager.grab_avg(self.bobber_cords)
        self.original_water_rgb = idle_bobber
        self.last_5_diffs = []

        while time.time() < self.find_start_time + 25:
            current_bobber = Imager.grab_avg(self.bobber_cords)
            self.scanning_water_rgb = current_bobber

            rgb_diff = Imager.rgb_distance(idle_bobber, current_bobber)
            self.add_diff(rgb_diff)

            if rgb_diff > self.bobber_sensitivity:
                return True
        return False

    def add_diff(self, val):
        self.last_5_diffs.insert(0,val)
        while (len(self.last_5_diffs)) > 5:
            self.last_5_diffs.pop()
