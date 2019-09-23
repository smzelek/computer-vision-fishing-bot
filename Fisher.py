import threading, time, sys
from Scanner import *
import Controller


# running data:

# Number of minutes elapsed
# Number of fish caught

# show historic img grab
# show current img grab
# scrolling text of diff number values
# colored red if below threshhold (skip)
# colored green if above (found)

# then change to a bobber monitoring view when found
# capture bobber img
# capture splash finding image
# scrolling text of diff number values

# play a happy sound when a fish was caught


class Fisher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.should_kill = False
        self.thing_done.set()
        self.can_run.set()    
        self.scanner = Scanner()

        self.finished = False
        self.num_fish_caught = 0
        self.start_time = 0
        self.pause_time = 0
        self.run_for_minutes = 0
        self.run_forever = False
        self.use_bauble = False
        self.bauble_duration_mins = 0
        self.last_used_bauble_time = 0
        self.cast_time = None


    def get_elapsed_time(self):
        if self.pause_time is not 0:
            return self.pause_time - self.start_time

        return time.time() - self.start_time

    def get_remaining_time(self):
        if self.pause_time is not 0:
            return (self.run_for_minutes * 60) - (self.pause_time - self.start_time)

        return (self.run_for_minutes * 60) - (time.time() - self.start_time) 

    def start(self, start, end, run_for_minutes, use_bauble, bauble_duration):
        self.scanner.start = start
        self.scanner.end = end
        self.scanner.scan_water()
        self.bauble_duration_mins = bauble_duration

        self.start_time = time.time()
        self.run_for_minutes = run_for_minutes
        if (run_for_minutes is 0):
            self.run_forever = True
        self.use_bauble = use_bauble
        threading.Thread(target=self.run).start()

    def run(self):
        while self.run_forever or self.get_remaining_time() > 0:
            self.can_run.wait()
            if self.should_kill:
                self.done_fishing()
            try:
                self.thing_done.clear()
                self.fish()
            finally:
                self.thing_done.set()
        self.done_fishing()

    def done_fishing(self):
        self.finished = True
        sys.exit()

    def fish(self):
        self.use_bauble_if_needed()
            
        Controller.cast()
        self.cast_time = time.time()
        time.sleep(3)

        if self.scanner.find_bobber():
            if self.scanner.wait_for_splash():
                Controller.set_mouse_pos(self.scanner.bobber_cords)
                time.sleep(0.06)
                Controller.loot()
                time.sleep(0.5)
                self.num_fish_caught = self.num_fish_caught + 1

    def use_bauble_if_needed(self):
        if self.use_bauble and (time.time() > self.bauble_duration_mins * 60 + self.last_used_bauble_time):
            Controller.use_bauble()
            self.last_used_bauble_time = time.time()

    def pause(self):
        self.scanner.should_kill = True
        self.pause_time = time.time()
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.scanner.should_kill = False
        self.start_time = self.start_time + (time.time() - self.pause_time)
        self.pause_time = 0
        self.can_run.set()

    def end(self):
        self.can_run.set()
        self.should_kill = True
        self.scanner.should_kill = True
