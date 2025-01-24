from tkinter import messagebox
from tkinter import *
from customtkinter import *
from app.utils.config import *
import orjson
from datetime import datetime, timezone, timedelta


def get_current_date():
    return datetime.today().date()


class JobRecords:

    def __init__(self, master):
        self.frame = CTkFrame(master)
        self.frame.grid(row=0, column=2, rowspan=2,
                        columnspan=3, sticky=NSEW, padx=20, pady=20)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.sidebar = JobRecordControls(self.frame, master)
        self.sidebar.set_record_field()


class JobRecordControls:
    """
    You will need to add another elif block at "clear_field" and "dump_records"
    when adding a new field in this class.
    """
    fields = ["record", "todo"]

    def __init__(self, master, pre_master):
        self.master = master
        self.pre_master = pre_master

        self.frame = CTkFrame(master)
        self.frame.grid(row=0, column=0, rowspan=3,
                        sticky=NSEW, padx=10, pady=10)

        self.current_field = self.fields[0]
        self.field = None

        CTkLabel(self.frame, text=JobRecords_.TITLE, font=CTkFont(size=20, weight="bold")
                 ).grid(row=0, column=0, padx=20, pady=10)

        cmd_list = [self.set_record_field, self.set_todo_field]
        for r_ind in range(len(JobRecords_.RECORDS)):
            CTkButton(self.frame, text=JobRecords_.RECORDS[r_ind], command=cmd_list[r_ind]).grid(
                row=1 + r_ind, column=0, padx=20, pady=10)

        self.save_btn = CTkButton(
            master, text=JobRecords_.SAVE_BTN_TEXT, command=self.save_records)
        self.save_btn.grid(row=2, column=2, sticky=E,
                           padx=(0, 10), pady=(0, 10))

        self.cancel_btn = CTkButton(
            master, text=JobRecords_.CLEAR_BTN_TEXT, fg_color="#888", hover_color="#AAA", command=self.clear_field)
        self.cancel_btn.grid(row=2, column=1, sticky=E,
                             padx=(0, 10), pady=(0, 10))

    def grid_field(self, field: CTkBaseClass):
        if self.field:
            self.field.destroy()
        self.field = field
        self.field.grid(row=0, column=1, rowspan=2,
                        columnspan=3, sticky=NSEW, padx=(0, 10), pady=10)

    def set_record_field(self):
        self.save_records()
        self.current_field = self.fields[0]

        self.grid_field(CTkTextbox(self.master))

        self.saved_record = self.fetch_current_record().get("record", "")

        self.field.insert(0., self.saved_record)

    def set_todo_field(self):
        self.save_records()
        self.current_field = self.fields[1]

        _frame = CTkFrame(self.master, fg_color="transparent")
        _frame.grid_rowconfigure(1, weight=1)
        _frame.grid_columnconfigure(1, weight=1)

        self.todo_frame = CTkScrollableFrame(_frame, fg_color=("#CCC", "#222"))
        self.todo_frame.grid(
            row=1, column=0, columnspan=2, sticky=NSEW)
        CTkButton(_frame, text=JobRecords_.NEW_TODO, command=self.add_todo).grid(
            row=0, column=0, sticky=NW, pady=(0, 10))

        self.saved_record = self.fetch_current_record().get("todo", [])
        self.todo_count = 0

        self.grid_field(_frame)

        self.todo_list = []
        if self.saved_record:
            for text in self.saved_record:
                self.add_todo(text)

    def grid_todo_fields(self, _frame, entry_default=None):
        _label = CTkLabel(_frame, text=f"{self.todo_count}.")
        _label.grid(
            row=0, column=0)

        _entry = CTkEntry(
            _frame, placeholder_text=JobRecords_.TODO_ENTRY_PLACEHOLDER, width=250)
        _entry.grid(
            row=0, column=1, columnspan=2, padx=10)
        if entry_default:
            _entry.delete(0, END)
            _entry.insert(0, entry_default)

        _btn = CTkButton(_frame, text=JobRecords_.REMOVE_TODO,
                         command=self.remove_todo(self.todo_count-1))
        _btn.grid(row=0, column=3)

        return _label, _entry, _btn

    def add_todo(self, default_text=None):
        _frame = CTkFrame(self.todo_frame, fg_color="transparent")
        _frame.grid(row=self.todo_count, column=0, sticky=EW, pady=(0, 10))
        _frame.grid_columnconfigure((1, 2), weight=1)

        self.todo_count += 1
        self.todo_list.append(
            [_frame, self.grid_todo_fields(_frame, default_text)])

    def __refresh_todo(self):
        for k, todo in enumerate(self.todo_list):
            self.todo_count = k+1
            todo[0].grid_forget()
            todo[0].grid(row=k, column=0,
                         sticky=EW, pady=(0, 10))
            entry_default = todo[1][1].get()
            for fields in todo[1]:
                fields.destroy()
            todo[1] = self.grid_todo_fields(todo[0], entry_default)

    def remove_todo(self, ind):
        def __remove_todo():
            todo_text = self.todo_list[ind][1][1].get()
            if len(todo_text) > 10:
                todo_text = todo_text[:10]+"..."
            if messagebox.askokcancel(JobRecords_
                                      .TODO_DEL_CONFRIM_TITLE,
                                      JobRecords_
                                      .TODO_DEL_CONFRIM_MESSAGE.format(todo_text)):
                self.todo_list.pop(ind)[0].destroy()
                self.__refresh_todo()
        return __remove_todo

    def clear_field(self):
        if self.current_field == self.fields[0]:
            self.field.delete(0., END)
        elif self.current_field == self.fields[1]:
            for e in todo_list:
                e.destroy()
            todo_list = []

    def fetch_current_record(self):
        return orjson.loads(self.pre_master.db.fetch_records(get_current_date()))

    def dump_records(self, records=dict()):
        if not self.field:
            return

        if self.current_field == self.fields[0]:
            records[self.fields[0]] = self.field.get(0., END)[:-1]
        elif self.current_field == self.fields[1]:
            records[self.fields[1]] = [e[1][1].get()
                                       for e in self.todo_list]
        return records

    def save_records(self):
        if not self.field:
            return

        records = self.fetch_current_record()

        self.pre_master.db.store_records(
            get_current_date(), self.dump_records(records))

    @property
    def is_saved(self):
        return self.dump_records()[self.current_field] == self.saved_record
