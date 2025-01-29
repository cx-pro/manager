import os
from tkinter import *
from customtkinter import *
from app.utils.config import *


class Contracts:
    def __init__(self, master):
        self.frame = CTkScrollableFrame(
            master, label_text="契約列表:")
        self.frame.grid(row=1, column=1, padx=(20, 0),
                        pady=(20, 0), sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.refresh_list()

    def open_file(self, path):
        def _open_file():
            os.startfile(path)
        return _open_file

    def refresh_list(self):
        self.frame_list = [(_label := CTkButton(master=self.frame,
                                                text=fn[:-fn[::-1].index(".")-1], command=self.open_file(APP_DIR + Contracts_.FOLDER_PATH + fn)),
                            _label.grid(row=_k, column=0, padx=10, pady=(0, 20)))[0]
                           for _k, fn in enumerate(os.listdir(Contracts_.FOLDER_PATH)) if os.path.isfile(Contracts_.FOLDER_PATH + fn)]
