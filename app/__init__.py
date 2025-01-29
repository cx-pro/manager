import os
from tkinter import *
from customtkinter import *
from app.utils.config import *
from app.utils.compoments.Sidebar import SideBar
from app.utils.compoments.Controls import Controls
from app.utils.compoments.Contracts import Contracts


class App(CTk):
    def __init__(self):
        super().__init__()

        set_appearance_mode("System")
        set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = SideBar(self)
        self.contracts = Contracts(self)
        self.controls = Controls(self)

        self.entry = CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0),
                        pady=(20, 20), sticky="nsew")

        self.main_button_1 = CTkButton(
            master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20),
                                pady=(20, 20), sticky="nsew")

        self.textbox = CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=2, padx=(20, 0),
                          pady=(20, 0), sticky="nsew")

        self.tabview = CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0),
                          pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(
            0, weight=1)
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                          values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.combobox_1 = CTkComboBox(self.tabview.tab("CTkTabview"),
                                      values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.string_input_button = CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                             command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.label_tab_2 = CTkLabel(self.tabview.tab(
            "Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.radiobutton_frame = CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20),
                                    pady=(20, 0), sticky="nsew")

        self.radio_var = IntVar(value=0)

        self.label_radio_group = CTkLabel(
            master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        self.radio_button_1 = CTkRadioButton(
            master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = CTkRadioButton(
            master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_3 = CTkRadioButton(
            master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.checkbox_slider_frame = CTkFrame(self)
        self.checkbox_slider_frame.grid(
            row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.checkbox_1 = CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0),
                             padx=20, sticky="n")

        self.checkbox_2 = CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0),
                             padx=20, sticky="n")

        self.checkbox_3 = CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()

        self.radio_button_3.configure(state="disabled")

        self.sidebar_frame.appearance_mode_optionemenu.set("跟隨系統")

        self.optionmenu_1.set("CTkOptionmenu")

        self.combobox_1.set("CTkComboBox")

        self.textbox.insert("0.0", "CTkTextbox\n\n" +
                            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def open_input_dialog_event(self):
        dialog = CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
