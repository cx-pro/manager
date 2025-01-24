import os


APP_NAME = "Manager"
APP_DIR = os.path.abspath(os.curdir)+"/"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600


class Sidebar:
    WEBSITE_LABEL = "外包網站"

    TASKER_LABEL = "Tasker 出任務"
    CASEPLUS_LABEL = "Case+ 外包網"
    FREELANCER_LABEL = "Freelancer"

    TASKER_URL = "https://www.tasker.com.tw/"
    CASEPLUS_URL = "https://case.1111.com.tw/"
    FREELANCER_URL = "https://www.freelancer.com/dashboard"

    APPEARANCE_LABEL = "外觀模式"
    APPEARANCE_LIST = ["明亮", "深色", "跟隨系統"]
    APPEARANCE_MAP = dict(zip(APPEARANCE_LIST, ["Light", "Dark", "System"]))


class Contracts_:
    LIST_LABEL = "契約列表:"
    TMP_FOLDER_PATH = "./contracts_templates/"


class Clients_:
    LIST_LABEL = "客戶列表:"
    PROCESSING_CLIENT_LABEL = "處理中客戶 : "
    CREATEING_WINDOW_TITLE = "新增客戶"
    CREATEING_WINDOW_NAME_ENTRY_PLACEHOLDER = "請輸入客戶名稱"
    NEW_CLIENT_BTN_LABEL = "新增客戶"
    SET_CLIENT_BTN_LABEL = "將選擇的客戶設為處理中"
    DELETE_CLIENT_BTN_LABEL = "移除已選擇客戶"


class Controls_:
    TAB_NAMES = ["契約管理", "客戶管理"]
    CONTRACT_NAME_ENTRY_PLACEHOLDER = "請輸入契約書名稱"
    CONTRACTS_TEMPLATES = ["不使用範本", "程式設計契約範本"]
    _OR = "或"
    CONTRACTS_MAP = dict(zip(CONTRACTS_TEMPLATES, [None,
                                                   f"{APP_DIR}{Contracts_.TMP_FOLDER_PATH}programming.odt"]))
    NEW_CONTRACT_BTN_LABEL = "創建新契約"
    IMPORT_CONTRACT_BTN_LABEL = "匯入契約檔案"
    CLICK_TO_SELECT_LABEL = "按一下以選擇"
    OPEN_CONTRACT_BTN_LABEL = "開啟已選擇契約"
    DELETE_CONTRACT_BTN_LABEL = "移除已選擇契約"
    START_WORKING_TIMER_BTN_LABEL = "開始計算工時"
    END_WORKING_TIMER_BTN_LABEL = "停止計算工時"
    TIMER_LABEL = "本客戶總計工作時間: {} 小時"


class JobRecords_:
    TITLE = "工作日誌"

    RECORDS = ["本日記事", "待辦事項"]
    FIELD_TYPES_MAP = dict(zip(["record", "todo"], RECORDS))

    NEW_TODO = "新增待辦事項"
    REMOVE_TODO = "刪除"
    TODO_ENTRY_PLACEHOLDER = "待辦事項"

    SAVE_BTN_TEXT = "儲存"
    CLEAR_BTN_TEXT = "清空"

    TODO_DEL_CONFRIM_TITLE = "確認刪除"
    TODO_DEL_CONFRIM_MESSAGE = "確定要刪除以下待辦事項？\n{}"

    SAVE_CONFIRM_ON_WINDOW_CLOSING_TITLE = "確認"
    SAVE_CONFIRM_ON_WINDOW_CLOSING_MESSAGE = "是否要儲存{}?"


class DB_:
    FOLDER_PATH = "./dbs/"

    RECORDS_TABLE_CREATE_SQL = "CREATE TABLE IF NOT EXISTS `Records` (`id` VARCHAR(50) PRIMARY KEY,`content` MEDIUMBLOB NOT NULL);"
    RECORDS_REMOVE_SQL = "DELETE FROM `Records` WHERE `id` = ? "
    RECORDS_STORE_SQL = "INSERT INTO `Records` (`id`,`content`) VALUES (?,?)"
    RECORDS_FETCH_SQL = "SELECT `content` FROM `Records` WHERE `id`=?"

    CONTRACTS_TABLE_CREATE_SQL = "CREATE TABLE IF NOT EXISTS `Contracts` (`name` VARCHAR(1000) PRIMARY KEY,`content` LONGBLOB NOT NULL);"
    CONTRACTS_REMOVE_SQL = "DELETE FROM `Contracts` WHERE `name` = ? "
    CONTRACTS_STORE_SQL = "INSERT INTO `Contracts` (`name`,`content`) VALUES (?,?)"
    CONTRACTS_FETCH_SQL = "SELECT `content` FROM `Contracts` WHERE `name`=?"
    CONTRACTS_FETCH_LIST_SQL = "SELECT `name` FROM `Contracts`"

    CLIENTS_TABLE_CREATE_SQL = "CREATE TABLE IF NOT EXISTS `Clients` (`id` INTEGER PRIMARY KEY AUTOINCREMENT,`name` VARCHAR(150),`work_time` INTEGER);"
    CLIENTS_REMOVE_SQL = "DELETE FROM `Clients` WHERE `id` = ?"
    CLIENTS_FETCH_SQL = "SELECT * FROM `Clients` WHERE `id`= ?"
    CLIENTS_FETCH_BY_NAME_SQL = "SELECT * FROM `Clients` WHERE `name`= ?"
    CLIENTS_FETCH_ALL_SQL = "SELECT * FROM `Clients`"
    CLIENTS_STORE_SQL = "INSERT INTO `Clients` (`name`,`work_time`) VALUES (?, ?)"
    CLIENTS_FETCH_WORK_HOUR_SQL = "SELECT `work_time` FROM `Clients` WHERE `id`=?"
    CLIENTS_STORE_WORK_HOUR_SQL = "UPDATE `Clients` SET `work_time`=? WHERE `id`=?"

    SETTINGS_TABLE_CREATE_SQL = "CREATE TABLE IF NOT EXISTS `Settings` (`name` VARCHAR(150) PRIMARY KEY,`val` VARCHAR(1000) NOT NULL);"
    SETTINGS_REMOVE_SQL = "DELETE FROM `Settings` WHERE `name` = ? "
    SETTINGS_FETCH_SQL = "SELECT `val` FROM `Settings` WHERE `name`= ?"
    SETTINGS_STORE_SQL = "INSERT INTO `Settings` (`name`,`val`) VALUES (?,?)"

    def __init__(self):
        self.DB_CONN = self.FOLDER_PATH + "main.db"

    def change_db(self, _db_conn, internal_db=True):
        self.DB_CONN = self.FOLDER_PATH + _db_conn if internal_db else _db_conn


class TEMP:
    FOLDER_PATH = "./temp/"
