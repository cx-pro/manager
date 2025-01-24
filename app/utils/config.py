APP_NAME = "Manager"

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

    APPEARANCE_LIST = ["明亮", "深色", "跟隨系統"]
    APPEARANCE_MAP = dict(zip(APPEARANCE_LIST, ["Light", "Dark", "System"]))
