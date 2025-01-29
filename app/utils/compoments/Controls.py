import os
from tkinter import *
from customtkinter import *
from app.utils.config import *
import shutil


class Controls:
    def __init__(self, master):
        self.master = master
        self.frame = CTkTabview(master, fg_color="transparent")
        self.frame.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.add_contract_tab()

    def add_contract_tab(self):
        tab_name = Controls_.TAB_NAMES[0]
        self.frame.add(tab_name)
        tab_obj = self.frame.tab(tab_name)
        tab_obj.grid_columnconfigure(0, weight=1)

        self.contract_tmp_option_menu = CTkOptionMenu(tab_obj,
                                                      values=Controls_.CONTRACTS_TEMPLATES)
        self.contract_tmp_option_menu.grid(
            row=0, column=0, padx=10, pady=(20, 0))

        # self.contract_name_entry = CTkEntry(tab_obj, placeholder_text=Controls_.CONTRACT_NAME_ENTRY_PLACEHOLDER)
        # self.contract_name_entry.grid(row=1, column=0, padx=10, pady=(20, 0))

        new_contract = CTkButton(master=tab_obj,
                                 text=Controls_.NEW_CONTRACT_BTN_LABEL, command=self.open_contract)
        new_contract.grid(row=2, column=0, padx=10, pady=(20, 0))

    def open_contract(self):
        dialog = self.get_new_contract_name()
        new_name = dialog.get_input()

        if not new_name:
            return

        tmp_path = Controls_.CONTRACTS_MAP[self.contract_tmp_option_menu.get()]
        new_path = f"{APP_DIR}{Contracts_.FOLDER_PATH}{new_name}.odt"

        if tmp_path:
            shutil.copyfile(tmp_path, new_path)
        else:
            with open(new_path, "w") as f:
                f.close()

        os.startfile(new_path)
        self.master.contracts.refresh_list()

    def get_new_contract_name(self):
        return CTkInputDialog(
            text=Controls_.CONTRACT_NAME_ENTRY_PLACEHOLDER, title=Controls_.CONTRACT_NAME_ENTRY_PLACEHOLDER)
