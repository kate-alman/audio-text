from additions import AppAddons, tk, ttk
from tkinter import Scrollbar


class UpdateWindow:

    def clear_window(self):
        for part in self.winfo_children():
            part.destroy()
        self.update()

    def text_window(self, text):
        UpdateWindow.clear_window(self)
        self.text_window = tk.Text(self, width=60, height=15, wrap='word')

        scroll_slider = Scrollbar(command=self.text_window.yview)
        scroll_slider.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_window.config(yscrollcommand=scroll_slider.set)
        self.text_window.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.text_window.insert(1.0, text)
        self.text_window.bind('<Control-a>', AppAddons.highlighting)

        self.box_of_languages = ttk.Combobox(self.main_window, font=self.main_font, state='readonly',
                                             values=[i for i in self.languages.keys()])
        self.box_of_languages.current(0)
        self.box_of_languages.pack(pady=3, padx=2, ipadx=10)

        UpdateWindow.text_buttons(self)
        self.update()

    def text_buttons(self):
        UpdateWindow.btn_save = tk.Button(self.main_window, text=f'Save file to... {chr(9835)}', font=self.main_font,
                                          bd=3, bg=self.main_theme,
                                          command=self.set_save_btn)
        UpdateWindow.btn_save.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=3, pady=3)
        UpdateWindow.btn_back = tk.Button(self.main_window, text='Back', font=self.main_font, bd=3, bg=self.main_theme,
                                          command=self.set_back_btn)
        UpdateWindow.btn_back.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=3, pady=3)
