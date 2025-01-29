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
    FOLDER_PATH = "./contracts/"
    TMP_FOLDER_PATH = "./contracts/templates/"


class Controls_:
    TAB_NAMES = ["契約管理"]
    CONTRACT_NAME_ENTRY_PLACEHOLDER = "請輸入契約書名稱"
    CONTRACTS_TEMPLATES = ["不使用範本", "程式設計契約範本"]
    CONTRACTS_MAP = dict(zip(CONTRACTS_TEMPLATES, [None,
                                                   f"{APP_DIR}{Contracts_.TMP_FOLDER_PATH}programming.odt"]))
    NEW_CONTRACT_BTN_LABEL = "創建新契約"


class LibreOffice:
    FOLDER_PATH = "./LibreOffice/"
