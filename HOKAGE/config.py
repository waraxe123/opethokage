import json
import os


def get_user_list(config, key):
    with open("{}/HOKAGE/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    LOGGER = True

    API_ID = ""
    API_HASH = ""
    ARQ_API_KEY = ""
    BOT_ID = ""
    TOKEN = ""
    OWNER_ID = "5513481385"
    OPENWEATHERMAP_ID = "22322"
    OWNER_USERNAME = "Mr_DiSasTer_XD"
    BOT_USERNAME = "HokageRobot"
    SUPPORT_CHAT = "TechQuardSupport"
    SUPPORT_CHANNEL = "TechQuard"
    JOIN_LOGGER = "-1001538788750"
    EVENT_LOGS = "-1001538788750"
    ERROR_LOG = "-1001538788750"

    SQLALCHEMY_DATABASE_URI = ""

    MONGO_DB_URL = ""  # needed for any database modules
    MONGO_URL = ""
    ARQ_API_URL = "https://arq.hamker.in"
    BOT_API_URL = "https://api.telegram.org/bot"
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""
    SPAMWATCH_SUPPORT_CHAT = "TechQuardSupport"

    REDIS_URL = ""

    DRAGONS = get_user_list("elevated_users.json", "sudos")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    REQUESTER = get_user_list("elevated_users.json", "whitelists")
    DEMONS = get_user_list("elevated_users.json", "supports")
    INSPECTOR = get_user_list("elevated_users.json", "sudos")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    DONATION_LINK = "https://t.me/Mr_DiSasTer_XD"
    CERT_PATH = None
    STRICT_GBAN = "True"
    PORT = ""
    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = 8
    BAN_STICKER = ""
    ALLOW_EXCL = True
    CASH_API_KEY = ""
    TIME_API_KEY = ""
    WALL_API = ""
    AI_API_KEY = ""
    BL_CHATS = []
    SPAMMERS = None
    SPAMWATCH_API = ""
    ALLOW_CHATS = None
    TEMP_DOWNLOAD_DIRECTORY = "./"
    HEROKU_APP_NAME = ""
    HEROKU_API_KEY = ""
    REM_BG_API_KEY = ""
    LASTFM_API_KEY = ""
    CF_API_KEY = ""
    BL_CHATS = []
    MONGO_PORT = "27017"
    MONGO_DB = "Hokage"
    PHOTO = ""
    TIME_API_KEY = ""
    INFOPIC = False


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

