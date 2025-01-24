import webbrowser
from tkinter import *
from customtkinter import *
from app.utils.config import *


class SideBar:
    def __init__(self, master):
        self.frame = CTkFrame(master, width=140, corner_radius=0)
        self.frame.grid(row=0, column=0, rowspan=2, sticky=NSEW)
        self.frame.grid_rowconfigure(5, weight=1)

        self.logo_label = CTkLabel(
            self.frame, text=APP_NAME, font=CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.freelance_websites_label = CTkLabel(
            self.frame, text=Sidebar.WEBSITE_LABEL)
        self.freelance_websites_label.grid(
            row=1, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = CTkButton(
            self.frame, text=Sidebar.TASKER_LABEL, command=self.open_web(Sidebar.TASKER_URL))
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_2 = CTkButton(
            self.frame, text=Sidebar.CASEPLUS_LABEL, command=self.open_web(Sidebar.CASEPLUS_URL))
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_3 = CTkButton(
            self.frame, text=Sidebar.FREELANCER_LABEL, command=self.open_web(Sidebar.FREELANCER_URL))
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = CTkLabel(
            self.frame, text=Sidebar.APPEARANCE_LABEL, anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = CTkOptionMenu(self.frame, values=Sidebar.APPEARANCE_LIST,
                                                         command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=7, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_optionemenu.set("跟隨系統")

    def open_web(self, url):
        def __open_web():
            webbrowser.open_new(url)
        return __open_web

    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(Sidebar.APPEARANCE_MAP[new_appearance_mode])
