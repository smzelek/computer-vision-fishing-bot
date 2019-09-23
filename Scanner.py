import Imager
from collections import OrderedDict
import time
import Controller

class Scanner():
    def __init__(self):
        self.start = 0
        self.end = 0
        self.should_kill = False

        self.status = 'Scanning.'
        self.water_values = OrderedDict()
        self.find_start_time = 0
        self.bobber_cords = None

        self.original_water_rgb = [0,0,0]
        self.scanning_water_rgb = [0,0,0]
        self.max_variant = 0
        self.water_sensitivity = 500
        self.bobber_sensitivity = 100

    def scan_water(self):
        y = self.start[1]
        while y < self.end[1]:
            x = self.start[0]
            while (x < self.end[0]):
                Controller.set_mouse_pos([x, y])
                check = Imager.grab_avg([x,y])
                self.water_values[(x,y)] = check
                x = x + 20
            y = y + 20

    def find_bobber(self):
        self.find_start_time = time.time()
        for key, value in self.water_values.items():
            if time.time() > self.find_start_time + 25:
                break
            if self.should_kill:
                break

            Controller.set_mouse_pos(key)
            scan_value = Imager.grab_avg(key)
            rgb_diff = Imager.rgb_distance(scan_value, value)
            
            self.original_water_rgb = value
            self.scanning_water_rgb = scan_value  
            self.status = 'Bobber: {} < {} ? '.format(self.water_sensitivity, rgb_diff)

            if rgb_diff > self.water_sensitivity:
                self.bobber_cords = key
                self.status = 'Bobber: {} < {} ? FOUND'.format(self.water_sensitivity, rgb_diff)
                return True
        return False

    def wait_for_splash(self):
        poll_start_time = time.time()
        idle_bobber = Imager.grab_avg(self.bobber_cords)
        self.max_variant = 0
        self.original_water_rgb = idle_bobber

        while time.time() < self.find_start_time + 25:
            if self.should_kill:
                break

            current_bobber = Imager.grab_avg(self.bobber_cords)
            rgb_diff = Imager.rgb_distance(idle_bobber, current_bobber)

            variance_ceiling = 1000
            if (rgb_diff > variance_ceiling):
                self.status = 'Splash: {} < {} FOUND'.format(variance_ceiling, rgb_diff)
                return True

            if time.time() < poll_start_time + 2:
                self.max_variant = max(self.max_variant, rgb_diff)

            self.scanning_water_rgb = current_bobber
            
            if (rgb_diff > self.max_variant + self.bobber_sensitivity):
                self.status = 'Splash: {} < {} FOUND'.format(self.max_variant + self.bobber_sensitivity, rgb_diff)
                return True
            else:
                self.status = 'Splash: {} < {} ?'.format(self.max_variant + self.bobber_sensitivity, rgb_diff)
                
        return False
