#!/usr/bin/env python3

import os
import sys
from tkinter import messagebox, filedialog, simpledialog
from update_window import UpdateWindow, AppAddons, tk
from idlelib.tooltip import Hovertip
import threading
import re
import textract
from PyPDF2 import PdfReader
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import gtts
from PIL import ImageTk, Image
from textract.exceptions import ShellError


class Application(tk.Tk):
    '''
    Hey! This is my first little project.
    If you have suggestions for improvement please send them to: ekaterina.alman@gmail.com. Thank you!

    Agreement (license).
    BeWare.
    You can:
    1) The Program can be distributed on any type of media and over the network;
    2) You can change the program in any way.
    Without changing the value of the ABOUT dialog.
    3) You can use the program as you wish.
    Create new versions, supplement and expand capabilities.
    Without changing the principle (!) of the program and without adding malicious functions.

    ABOUT: kate-alman, ekaterina.alman@gmail.com, https://github.com/kate-alman
    '''

    def __init__(self):
        tk.Tk.__init__(self)
        self.main_theme = '#F8F8FF'
        self.main_font = ("Arial Rounded MT Bold", 10)
        self.configure(highlightthickness=1, bg=self.main_theme)

        self.title('Get-Audio-from-Text')
        self.iconphoto(False, tk.PhotoImage(file=r'images/icons8.png'))
        self.languages = {'Choose language': 'ru', 'Russian': 'ru', 'English': 'en', 'French': 'fr', 'Spanish': 'es',
                          'Portuguese': 'pt', 'Mandarin (China Mainland)': 'zh-CN',
                          'Mandarin (Taiwan)': 'zh-TW'}
        self.image_connect = ImageTk.PhotoImage(
            Image.open(r'images/connected.png').resize((25, 25)))

        self.set_ui()

    def set_ui(self):
        self.main_window = tk.Frame(self, bg='#F8F8FF').pack(fill=tk.X, expand=False)
        self.minsize(width=150, height=220)
        self.wm_attributes('-alpha', 1.0)

        _ABOUT = tk.Label(self.main_window, text=f'by kate-alman',
                              bg=self.main_theme).pack(side=tk.BOTTOM)

        self.greeting = tk.Label(self.main_window, text=f'Hello, \nwhat first?', width=15, height=3,
                                 font=("Arial Rounded MT Bold", 15, "bold"), bd=3, bg=self.main_theme)
        self.greeting.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.btn_open_file = tk.Button(self.main_window, text='Open file',
                                       font=self.main_font, bd=3, bg=self.main_theme,
                                       command=self.set_openfile_btn, width=12)
        self.btn_open_file.pack(fill=tk.BOTH, padx=5, pady=5)

        self.btn_write_text = tk.Button(self.main_window, text='Write text',
                                        font=self.main_font, bd=3, bg=self.main_theme,
                                        command=self.set_writetext_btn, width=12)
        self.btn_write_text.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)

        self.btn_open_url = tk.Button(self.main_window, text='Open text from link',
                                      font=self.main_font, bd=3, bg=self.main_theme,
                                      command=self.set_open_url, width=12)
        self.btn_open_url.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)

        self.set_bt()

        self.thread_connect = threading.Thread(target=self.check_network_connection, args=(), daemon=True)
        self.thread_connect.start()

        self.update()

    def set_bt(self):
        self.bar_navigation = tk.Frame(self, bg=self.main_theme).pack(fill=tk.X)

        self.btn_instruction = tk.Button(self.bar_navigation, text='Instruction',
                                         font=self.main_font, bd=3, bg=self.main_theme,
                                         command=self.set_instruct_btn, width=12)
        self.btn_instruction.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

        self.btn_exit = tk.Button(self.bar_navigation, text='Exit',
                                  font=self.main_font, bd=3, bg=self.main_theme,
                                  command=self.set_exit_btn, width=12)
        self.btn_exit.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

    def set_openfile_btn(self):
        ftypes = [('Text files', ['*.txt', '*.doc', '*.docx', '*.pdf']), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        file_open = dlg.show()

        try:
            if re.search(r'.do[c|x]', file_open):
                text = textract.process(file_open)
                text = text.decode('utf-8')
            elif re.search(r'.pdf', file_open):
                text = PdfReader(file_open)
                pages = []
                for page in range(len(text.pages)):
                    pages.append(text.pages[page].extract_text())
                text = pages
            else:
                with open(file_open, encoding='utf-8') as file:
                    text = file.read()
            UpdateWindow.text_window(self, text)

        except ShellError:
            messagebox.showinfo('Text not found', f'Sorry! Text not found.\nPlease try another file.')

        except FileNotFoundError:
            pass

    def set_writetext_btn(self):
        text = '---Enter text---'
        UpdateWindow.text_window(self, text)

    def set_open_url(self):
        try:
            url = simpledialog.askstring(title='Enter link', prompt="Enter link")
            if url:
                html = urlopen(Request(url)).read()
                soup = BeautifulSoup(html, features="html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                UpdateWindow.text_window(self, text)
            else:
                messagebox.showinfo('Instruction', 'Enter URL')

        except HTTPError as err:
            messagebox.showinfo('Error', f'Error {err.code, err.reason}')
        except ValueError:
            messagebox.showinfo('No URL', f'URL not entered')

    @staticmethod
    def set_instruct_btn():
        instuction_text = '''
        Hello friend! 
        Here you can save the audio file from the entered text.
        ------------------------------------------------------
        You can open files in the following formats: 
        .txt, .doc, .docx, .pdf.
        You can write the text yourself.
        And also you can download the text from any site!
        ------------------------------------------------------
        To save the file, just click on the save button. 
        Default save language is russian, 
        you can choose any other from the list.
        You need internet to save the file correctly!
        If you want to return to the main window, 
        just press the button.
        ------------------------------------------------------
        Thank you for using this program!
        If you have suggestions for improvement please 
        send them to: ekaterina.alman@gmail.com
        '''
        messagebox.showinfo('Instruction', instuction_text)

    def set_back_btn(self):
        UpdateWindow.clear_window(self)
        self.set_ui()

    def set_exit_btn(self):
        self.destroy()
        sys.exit()

    def check_network_connection(self):
        '''
        Thanks to Icons8 (https://icons8.com) Wi-Fi Connected - icon (https://icons8.com/icon/110274/wi-fi-connected)
        '''

        try:
            response = urlopen('https://google.com', timeout=1)
            if response:
                self.status_connection = tk.Label(self.main_window, bg=self.main_theme, image=self.image_connect)
                self.status_connection.pack(fill=tk.BOTH, padx=2)
                Hovertip(self.status_connection, "Internet is up", hover_delay=100)

        except (URLError, RuntimeError):
            pass

    def set_save_btn(self):
        self.thread_slider = threading.Thread(target=self.save_file, args=())
        self.thread_slider.start()
        UpdateWindow.btn_save['state'] = 'disabled'
        UpdateWindow.btn_back['state'] = 'disabled'

    def save_file(self):
        with open('tmp_textfile.txt', 'w', encoding='utf-8') as tmp_file:
            tmp_file.write(self.text_window.get('1.0', 'end'))

        with open('tmp_textfile.txt', encoding='utf-8') as tmp_fl:
            t = tmp_fl.read()
            s = gtts.gTTS(t, lang=self.languages[list(self.languages.keys())[self.box_of_languages.current()]])

            try:
                AppAddons.saved_slider(self)
                self.wm_attributes('-alpha', 0.1)

                s.save(filedialog.asksaveasfilename(defaultextension=".mp3",
                                                    filetypes=[("Audio .mp3", ".mp3"),
                                                               ("Audio .wav", ".wav")],
                                                    initialdir="dir",
                                                    title="Save as"))
                messagebox.showinfo('Instruction', 'Saved')
                AppAddons.update_after_exception(self)

            except gtts.tts.gTTSError:
                messagebox.showinfo('Connection error', 'Error, please check your internet connection and try again')
                AppAddons.update_after_exception(self)

            except FileNotFoundError:
                AppAddons.update_after_exception(self)

        os.remove('tmp_textfile.txt')
        UpdateWindow.btn_save['state'] = 'normal'
        UpdateWindow.btn_back['state'] = 'normal'


if __name__ == '__main__':
    root = Application()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
