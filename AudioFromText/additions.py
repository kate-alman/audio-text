import tkinter as tk
from tkinter import ttk


class AppAddons:

    def highlighting(self, event):
        self.text_window.tag_add(tk.SEL, "1.0", 'end')
        self.text_window.mark_set(tk.INSERT, "1.0")
        self.text_window.see(tk.INSERT)
        return 'break'

    def saved_slider(self):
        self.bar_slider = tk.Toplevel()
        self.wm_attributes('-alpha', 1.0)

        x = (self.bar_slider.winfo_screenwidth() - self.bar_slider.winfo_reqwidth()) / 2
        y = (self.bar_slider.winfo_screenheight() - self.bar_slider.winfo_reqheight()) / 2
        self.bar_slider.geometry("+%d+%d" % (x, y))
        self.bar_slider_title = tk.Label(self.bar_slider, text='Please don\'t close window').pack()
        self.bar_slider.overrideredirect(True)

        self.running_bar_slider = ttk.Progressbar(self.bar_slider, mode="determinate")
        self.running_bar_slider.pack(side=tk.TOP)
        self.running_bar_slider.start()
        self.running_bar_slider.step(10)

    def update_after_exception(self):
        self.bar_slider.destroy()
        self.wm_attributes('-alpha', 1.0)
        self.update()
