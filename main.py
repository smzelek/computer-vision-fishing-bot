from PIL import Image, ImageTk
from Fisher import *
from PauseListener import *
import Controller
import Imager
import Tkinter 
import sys 
import os
import datetime
import math

class Main():
    def __init__(self):
        self.fisher = Fisher()
        self.start = None
        self.end = None
        self.use_bauble = False
        self.run_for_minutes = 0
        self.bauble_duration = 0
        self.is_paused = False
        self.pause_listener = PauseListener(self.toggle_pause)

    def create_setup_gui(self):
        mainwindow = Tkinter.Tk()
        mainwindow.title('Gone Fishing') 
        mainwindow.wm_attributes("-topmost", 1)
        mainwindow.protocol("WM_DELETE_WINDOW", sys.exit)

        start_text = Tkinter.StringVar()
        end_text = Tkinter.StringVar()
        run_time_text = Tkinter.StringVar()
        run_time_text.set("0")
        bauble_flag = Tkinter.IntVar()
        bauble_duration = Tkinter.StringVar()
        bauble_duration.set("0")

        Tkinter.Label(mainwindow, text="Cast Start").grid(row=0)
        Tkinter.Label(mainwindow, textvariable=start_text).grid(row=0, column=1)
    
        Tkinter.Label(mainwindow, text="Casting End").grid(row=1)
        Tkinter.Label(mainwindow, textvariable=end_text).grid(row=1, column=1)

        Tkinter.Label(mainwindow, text='Fish For').grid(row=2, column=0)
        Tkinter.Entry(mainwindow, textvariable=run_time_text, width=5).grid(row=2, column=1)
        Tkinter.Label(mainwindow, text='Minutes').grid(row=2, column=2)

        Tkinter.Label(mainwindow, text='Use Bauble?').grid(row=3, column=0)
        Tkinter.Checkbutton(mainwindow, text="", variable=bauble_flag).grid(row=3, column=1)
        
        Tkinter.Label(mainwindow, text='Bauble Duration').grid(row=4, column=0)
        Tkinter.Entry(mainwindow, textvariable=bauble_duration, width=5).grid(row=4, column=1)
        
        image = Image.open("play.png").resize((25,25), Image.ANTIALIAS)
        play = ImageTk.PhotoImage(master=mainwindow, image=image)
        startButton = Tkinter.Button(mainwindow, text='', image=play, state="disabled", command=lambda:self.finish_setup(mainwindow, int(run_time_text.get()), bauble_flag.get(), int(bauble_duration.get())))

        Tkinter.Button(mainwindow, text='Set Mouse Start', width=25, command=lambda:self.set_mouse_start(start_text, startButton)).grid(row=5, columnspan=3)
        Tkinter.Button(mainwindow, text='Set Mouse End', width=25, command=lambda:self.set_mouse_end(end_text, startButton)).grid(row=6, columnspan=3)

        startButton.grid(row=7, columnspan=3)
        
        mainwindow.mainloop()

    def toggle_pause(self):
        if self.is_paused:
            self.resume_fishing()
            self.is_paused = False
        else:
            self.pause_fishing()
            self.is_paused = True

    def finish_setup(self, mainwindow, run_for_minutes, use_bauble, bauble_duration):
        mainwindow.destroy()
        self.bauble_duration = bauble_duration
        self.run_for_minutes = run_for_minutes
        self.use_bauble = use_bauble

    def set_mouse_start(self, text, start_button):
        Controller.wait_for_click()
        time.sleep(0.1)
        self.start = Controller.get_cords()
        text.set('({}, {})'.format(self.start[0], self.start[1]))
        if (self.end and self.start):
            start_button.config(state="normal")
        
    def set_mouse_end(self, text, start_button):
        Controller.wait_for_click()
        time.sleep(0.1)
        self.end = Controller.get_cords()
        text.set('({}, {})'.format(self.end[0], self.end[1]))
        if (self.end and self.start):
            start_button.config(state="normal")

    def create_running_gui(self):
        mainwindow = Tkinter.Tk()
        mainwindow.title('Gone Fishing') 
        mainwindow.wm_attributes("-topmost", 1)
        mainwindow.protocol("WM_DELETE_WINDOW", lambda:self.quit_fishing(mainwindow))

        image = Image.open("pause.png").resize((25,25), Image.ANTIALIAS)
        pause = ImageTk.PhotoImage(image)
        
        image = Image.open("play.png").resize((25,25), Image.ANTIALIAS)
        play = ImageTk.PhotoImage(image)

        Tkinter.Button(mainwindow, image=play, command=self.resume_fishing).pack(side="left")
        Tkinter.Button(mainwindow, image=pause, command=self.pause_fishing).pack(side="left")

        time_text = Tkinter.StringVar()
        Tkinter.Label(textvariable=time_text).pack(side="left")
        
        fish_text = Tkinter.StringVar()
        Tkinter.Label(textvariable=fish_text).pack(side="left")

        original_canvas = Tkinter.Canvas(mainwindow, width=20, height=20)
        original_canvas_element = original_canvas.create_rectangle(0, 0, 20, 20, fill="black")
        original_canvas.pack(side="left")
        
        compared_canvas = Tkinter.Canvas(mainwindow, width=20, height=20)
        compared_canvas_element = compared_canvas.create_rectangle(0, 0, 20, 20, fill="black")
        compared_canvas.pack(side="left")

        diff_text = Tkinter.StringVar()
        Tkinter.Label(textvariable=diff_text).pack(side="left")

        self.update_fields(mainwindow, time_text, fish_text, original_canvas, original_canvas_element, compared_canvas, compared_canvas_element, diff_text)
        mainwindow.mainloop()

    def create_summary_GUI(self):
        mainwindow = Tkinter.Tk()
        mainwindow.title('Gone Fishing') 
        mainwindow.wm_attributes("-topmost", 1)
        mainwindow.protocol("WM_DELETE_WINDOW", mainwindow.destroy)

        fishCaught = self.fisher.num_fish_caught
        elapsedTime = math.ceil(self.fisher.get_elapsed_time())
        elapsedTimestamp = str(datetime.timedelta(seconds=elapsedTime))
        avgFishRate = int(float(fishCaught) / elapsedTime * 3600) 
        summaryText = 'Caught {} fish in {}. Thats an average of {} fish per hour.'.format(fishCaught, elapsedTimestamp, avgFishRate)
        Tkinter.Label(text="Done Fishing!").pack(side="left")
        Tkinter.Label(text=summaryText).pack(side="left")        

        mainwindow.mainloop()

    def update_fields(self, mainwindow, time_text, fish_text, original_canvas, original_canvas_element, compared_canvas, compared_canvas_element, diff_text):
        if (self.fisher.finished):
            mainwindow.destroy()
            return1

        display_time = ""

        if (self.fisher.run_forever):
            display_time = str(datetime.timedelta(seconds=math.ceil(self.fisher.get_elapsed_time())))
        else:
            display_time = str(datetime.timedelta(seconds=math.ceil(self.fisher.get_remaining_time())))
        
        time_text.set(display_time)
        fish_text.set('{} fish.'.format(self.fisher.num_fish_caught))

        orig_hex = Imager.rgb_to_hex(self.fisher.scanner.original_water_rgb)
        original_canvas.itemconfig(original_canvas_element, fill=orig_hex)

        compare_hex = Imager.rgb_to_hex(self.fisher.scanner.scanning_water_rgb)
        compared_canvas.itemconfig(compared_canvas_element, fill=compare_hex)

        diff_text.set(self.fisher.scanner.status)

        mainwindow.after(100, lambda:self.update_fields(mainwindow, time_text, fish_text, original_canvas, original_canvas_element, compared_canvas, compared_canvas_element, diff_text))

    def quit_fishing(self, mainwindow):
        self.fisher.end()
        mainwindow.destroy()

    def start_fishing(self):
        self.fisher.start(self.start, self.end, self.run_for_minutes, self.use_bauble, self.bauble_duration)

    def resume_fishing(self):
        self.fisher.resume()
        self.is_paused = False

    def pause_fishing(self):
        self.fisher.pause()
        self.is_paused = True

if __name__ == '__main__':
    m = Main()
    m.create_setup_gui()
    m.start_fishing()
    m.create_running_gui()
    m.create_summary_GUI()