import os
import shutil
from tkinter import *
from customtkinter import *
from app.utils.config import *
from tkinter import filedialog
from threading import Thread
from time import time, sleep


class Controls:

    def __init__(self, master):
        self.master = master
        self.frame = CTkTabview(master, command=self.on_tab_changed)
        self.frame.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky=NSEW)

        self.control_lists = Control_list(master, self)

        self.tab_load_function = list(
            map(self.control_lists.get_show_list_func, range(2)))

        self.add_contract_tab()
        self.add_client_tab()

    def on_tab_changed(self):
        self.tab_load_function[Controls_.TAB_NAMES.index(self.frame.get())]()

    # vvv Management of Clients vvv
    def refresh_processing_client(self):
        self.client_label.configure(
            text=f"{Clients_.PROCESSING_CLIENT_LABEL}{self.master.db.fetch_clients(self.master.client)[1]}")

    def add_client_tab(self):
        tab_name = Controls_.TAB_NAMES[1]
        self.frame.add(tab_name)
        tab_obj = self.frame.tab(tab_name)
        tab_obj.grid_columnconfigure((0, 1), weight=1)

        self.client_label = CTkLabel(
            tab_obj, text=f"{Clients_.PROCESSING_CLIENT_LABEL}{self.master.db.fetch_clients(self.master.client)[1]}")
        self.client_label.grid(row=0, column=0, padx=10,
                               pady=(20, 0), sticky=W)
        self.timer_label = CTkLabel(
            tab_obj)
        self.timer_label.grid(row=0, column=1, padx=10, pady=(20, 0), sticky=E)

        self.new_client_btn = CTkButton(
            tab_obj, text=Clients_.NEW_CLIENT_BTN_LABEL, command=self.create_client)
        self.new_client_btn.grid(row=1, column=0, padx=10, pady=(20, 0))

        self.new_client_btn = CTkButton(
            tab_obj, text=Clients_.DELETE_CLIENT_BTN_LABEL, command=self.remove_selected_client)
        self.new_client_btn.grid(row=1, column=1, padx=10, pady=(20, 0))

        self.set_client_btn = CTkButton(
            tab_obj, text=Clients_.SET_CLIENT_BTN_LABEL, command=self.set_client)
        self.set_client_btn.grid(
            row=2, column=0, padx=10, pady=(20, 0), columnspan=2)

        self.start_working_timer = CTkButton(
            tab_obj, text=Controls_.START_WORKING_TIMER_BTN_LABEL, command=self.start_timer)
        self.start_working_timer.grid(row=3, column=0, padx=10, pady=(20, 0))

        self.end_working_timer = CTkButton(
            tab_obj, text=Controls_.END_WORKING_TIMER_BTN_LABEL, command=self.end_timer)
        self.end_working_timer.grid(row=3, column=1, padx=10, pady=(20, 0))

        self.selected_client = self.master.client
        self.timer = None
        self.work_during = self.init_work_during = self.master.db.fetch_work_time_by_client_id(
            self.selected_client)
        self.refresh_timer_label(self.work_during)

    def create_client(self):
        dialog = self.master.get_new_client_name()
        client_name = dialog.get_input()
        if not client_name:
            return
        self.master.client = self.master.db.store_client((client_name, 0))
        self.control_lists.refresh_list()

    def set_select_client(self, ind, btn_ind):
        def __select_client():
            self.control_lists.refresh_list(btn_ind)
            self.selected_client = ind
        return __select_client

    def set_client(self):
        self.master.client = self.selected_client
        self.refresh_processing_client()

    def remove_selected_client(self):
        self.master.db.delete_client_by_id(self.selected_client)
        self.master.client = None  # Value set to None will get the first client in db
        self.selected_client = self.master.client
        self.refresh_processing_client()
        self.control_lists.refresh_list()

    def refresh_timer_label(self, during):
        if during:
            self.timer_label.configure(
                text=Controls_.TIMER_LABEL.format(round(during/60/60)))
            return

    def start_timer(self):
        self.end_timer()
        sleep(.5)
        self._start_time = time()
        self.timer_run = True

        def __timer():
            while 1:
                sleep(.3)
                during = round(time() - self._start_time) \
                    + self.init_work_during
                if during > self.work_during:
                    self.work_during = during
                    self.refresh_timer_label(self.work_during)
                if not self.timer_run:
                    break

        self.timer = Thread(target=__timer)
        self.timer.start()

    def end_timer(self):
        if not self.timer:
            return
        self.timer_run = False
        self.timer.join()
        self.init_work_during = self.work_during
        self.work_during = 0
        self.timer = None
        self.master.db.store_work_time_by_client_id(
            self.master.client, self.init_work_during)

        self.refresh_timer_label(self.work_during)

    # ^^^ Management of Clients ^^^

    # vvv Management of Contracts vvv

    def add_contract_tab(self):
        tab_name = Controls_.TAB_NAMES[0]
        self.frame.add(tab_name)
        tab_obj = self.frame.tab(tab_name)
        tab_obj.grid_columnconfigure(0, weight=1)

        scrollable_frame = CTkScrollableFrame(tab_obj)
        scrollable_frame.grid(row=0, column=0, sticky=NSEW)
        scrollable_frame.grid_columnconfigure((0, 1), weight=1)

        self.open_contract_btn = CTkButton(
            scrollable_frame, text=Controls_.OPEN_CONTRACT_BTN_LABEL, command=self.control_lists.open_file)
        self.open_contract_btn.grid(
            row=0, column=0, padx=10, pady=(20, 0))

        self.open_contract_btn = CTkButton(
            scrollable_frame, text=Controls_.DELETE_CONTRACT_BTN_LABEL, command=self.remove_selected_contracts)
        self.open_contract_btn.grid(
            row=0, column=1, padx=10, pady=(20, 0))

        CTkLabel(scrollable_frame, text=Controls_._OR).grid(
            row=1, column=0, padx=10, pady=(20, 0), columnspan=2)

        import_contract = CTkButton(master=scrollable_frame,
                                    text=Controls_.IMPORT_CONTRACT_BTN_LABEL, command=self.import_contract)
        import_contract.grid(row=2, column=0, padx=10,
                             pady=(20, 0), columnspan=2)

        self.contract_tmp_option_menu = CTkOptionMenu(scrollable_frame,
                                                      values=Controls_.CONTRACTS_TEMPLATES)
        self.contract_tmp_option_menu.grid(
            row=3, column=0, padx=10, pady=(20, 0))

        new_contract = CTkButton(master=scrollable_frame,
                                 text=Controls_.NEW_CONTRACT_BTN_LABEL, command=self.open_contract)
        new_contract.grid(row=3, column=1, padx=10, pady=(20, 0))

        self.selected_contracts = []
        self.selected_contracts_ind = []

    def import_contract(self):
        for fn in filedialog.askopenfilenames():
            with open(fn, mode="rb") as f:
                self.master.db.store_contract(fn, f.read())
                f.close()
        self.control_lists.refresh_list()

    def set_select_contract(self, fn, btn_ind):
        def __select_contract():
            if btn_ind in self.selected_contracts_ind:
                self.selected_contracts_ind.remove(btn_ind)
                self.selected_contracts.remove(fn)
            else:
                self.selected_contracts_ind.append(btn_ind)
                self.selected_contracts.append(fn)

            self.control_lists.refresh_list(self.selected_contracts_ind)
        return __select_contract

    def open_contract(self):
        dialog = self.get_new_contract_name()
        new_name = dialog.get_input()

        if not new_name:
            return

        tmp_path = Controls_.CONTRACTS_MAP[self.contract_tmp_option_menu.get()]
        new_path = f"{APP_DIR}{TEMP.FOLDER_PATH}{new_name}.odt"

        if tmp_path:
            shutil.copyfile(tmp_path, new_path)
        else:
            with open(new_path, "w") as f:
                f.close()

        self.master.db.store_contract(new_path, "".encode())

        os.startfile(new_path)
        self.control_lists.refresh_list()

    def get_new_contract_name(self):
        return CTkInputDialog(
            text=Controls_.CONTRACT_NAME_ENTRY_PLACEHOLDER,
            title=Controls_.CONTRACT_NAME_ENTRY_PLACEHOLDER)

    def remove_selected_contracts(self):
        for fn in self.selected_contracts:
            self.master.db.delete_contracts_by_name(fn)
        self.control_lists.refresh_list()
        self.selected_contracts = self.selected_contracts_ind = []

    # ^^^ Management of Contracts ^^^


class Control_list:

    list_types = ["contracts", "clients"]

    def __init__(self, master, controls: Controls):
        self.master = master
        self.controls = controls
        self.frame = CTkScrollableFrame(
            master, fg_color="transparent")
        self.frame.grid(row=1, column=1, padx=(20, 0),
                        pady=20, sticky=NSEW)
        self.frame.grid_columnconfigure(0, weight=1)

        self.item_list = []

        self.show_list(0)

    def get_show_list_func(self, type_index):
        return lambda: self.show_list(type_index)

    def show_list(self, type_index):
        if type_index == 0:
            self.frame.configure(label_text=Contracts_.LIST_LABEL)
        elif type_index == 1:
            self.frame.configure(label_text=Clients_.LIST_LABEL)

        self.current_list = self.list_types[type_index]
        self.refresh_list()

    def open_file(self):
        self.master.save_changed_temps()
        for fn in self.controls.selected_contracts:
            file_bytes = self.master.db.fetch_contracts(fn)
            fp = APP_DIR + TEMP.FOLDER_PATH + fn
            with open(fp, "wb") as wf:
                wf.write(file_bytes)
                wf.close()
            os.startfile(fp)

    def destroy_items(self):
        for it in self.item_list:
            it.destroy()

    def refresh_contract_list(self, colored):
        CTkLabel(master=self.frame, text=Controls_.CLICK_TO_SELECT_LABEL).grid(
            row=0, column=0, pady=(0, 20), sticky=EW)

        def __get_kwargs(_k, fn: str):
            return {"master": self.frame,
                    "text": fn[:-fn[::-1].index(".")-1],
                    "command": self.controls.set_select_contract(fn, _k),
                    "fg_color": ["#36719F", "#144870"]} \
                if _k in colored else {"master": self.frame,
                                       "text": fn[:-fn[::-1].index(".")-1],
                                       "command": self.controls.set_select_contract(fn, _k)}
        self.item_list = [(_label := CTkButton(**__get_kwargs(_k, fn)),
                           _label.grid(row=_k+1, column=0, pady=(0, 20), sticky=EW))[0]
                          for _k, fn in enumerate(self.master.db.fetch_contracts()) if fn]

    def refresh_client_list(self, colored):
        CTkLabel(master=self.frame, text=Controls_.CLICK_TO_SELECT_LABEL).grid(
            row=0, column=0, pady=(0, 20), sticky=EW)

        def __get_kwargs(_k, cl):
            return {"master": self.frame,
                    "text": cl[1],
                    "command": self.controls.set_select_client(cl[0], _k)} \
                if _k != colored else {"master": self.frame,
                                       "text": cl[1],
                                       "command": self.controls.set_select_client(cl[0], _k),
                                       "fg_color": ["#36719F", "#144870"]}
        self.item_list = [(_label := CTkButton(**__get_kwargs(_k, cl)),
                           _label.grid(row=_k+1, column=0, pady=(0, 20), sticky=EW))[0]
                          for _k, cl in enumerate(self.master.db.fetch_clients()) if cl]

    def refresh_list(self, colored=None):
        self.destroy_items()
        if self.current_list == self.list_types[0]:
            self.refresh_contract_list(colored if colored != None else [])
        elif self.current_list == self.list_types[1]:
            self.refresh_client_list(colored if colored != None else -1)
