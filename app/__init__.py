from tkinter import *
from app.utils.db import DB
from customtkinter import *
from app.utils.config import *
from tkinter import messagebox
from app.utils.compoments.Sidebar import SideBar
from app.utils.compoments.Controls import Controls
from app.utils.compoments.JobRecords import JobRecords


class App(CTk):
    view_types = ["Contracts and JobRecords"]

    def __init__(self):
        self.prepare_folders()
        super().__init__()

        set_appearance_mode("System")
        set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.grid_columnconfigure((2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.current_view = self.view_types[0]
        self.db_config = DB_()
        self.db = DB(self, self.db_config)

        self.sidebar_frame = SideBar(self)
        self.controls = Controls(self)
        self.job_records = JobRecords(self)

        self.protocol("WM_DELETE_WINDOW", self.on_window_closing)

    def get_new_client_name(self):
        return CTkInputDialog(
            text=Clients_.CREATEING_WINDOW_NAME_ENTRY_PLACEHOLDER,
            title=Clients_.CREATEING_WINDOW_TITLE)

    @property
    def client(self):
        _client = self.db.fetch_setting("client")
        if not _client:
            _clients = self.db.fetch_clients()
            if not _clients:
                dialog = self.get_new_client_name()
                client_name = dialog.get_input()
                if not client_name:
                    exit()
                _client = self.db.store_client((client_name, 0))
            else:
                _client = _clients[0][0]

        return _client

    @client.setter
    def client(self, val):
        if val == None:
            _client = self.db.fetch_setting("client")
            _clients = self.db.fetch_clients()
            if not (_client and _client in [_[0] for _ in _clients]):
                if not _clients:
                    dialog = self.get_new_client_name()
                    client_name = dialog.get_input()
                    if not client_name:
                        exit()
                    val = self.db.store_client((client_name, 0))
                else:
                    val = _clients[0][0]

        self.db.store_setting("client", val)

    def prepare_folders(self):
        for fp in [DB_.FOLDER_PATH, TEMP.FOLDER_PATH, Contracts_.TMP_FOLDER_PATH]:
            if not os.path.isdir(fp):
                os.mkdir(fp)

    def save_changed_temps(self):
        for fn in os.listdir(TEMP.FOLDER_PATH):
            with open(TEMP.FOLDER_PATH + fn, "rb") as f:
                fd = f.read()
                f.close()
            if self.db.fetch_contracts(fn) != fd:
                self.db.store_contract(fn, fd)
            os.remove(TEMP.FOLDER_PATH + fn)
            del fd

    def on_window_closing(self):
        self.save_changed_temps()
        if self.current_view == self.view_types[0] and not self.job_records.sidebar.is_saved:
            if messagebox.askokcancel(JobRecords_
                                      .SAVE_CONFIRM_ON_WINDOW_CLOSING_TITLE,
                                      JobRecords_
                                      .SAVE_CONFIRM_ON_WINDOW_CLOSING_MESSAGE.format(
                                          JobRecords_
                                          .FIELD_TYPES_MAP[self.job_records.sidebar.current_field])):
                self.job_records.sidebar.save_records()
        self.destroy()
