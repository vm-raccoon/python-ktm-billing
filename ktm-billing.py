from classes.Config import Config
from classes.KTM import KTM
from classes.Database import Database as DB
from classes.TelegramBot import TelegramBot
from datetime import date


def compareDateToday(dt):
    return date.today().strftime("%Y-%m-%d") == dt[:10]


for item in Config(__file__, "config.json").read():
    db = DB(item["sqlite"])
    lastRow = db.getLastHistoryRow()

    if lastRow and compareDateToday(lastRow["datetime"]):
        continue

    overview = KTM(item["ktm-account"]).getOverview()
    db.insert(overview)

    overviewCopy = overview.copy()
    overviewCopy["username"] = item["ktm-account"]["username"]
    overviewCopy["diff"] = round(lastRow["balance"] - overview["balance"], 2) if lastRow else 0

    bot = TelegramBot(item["telegram"]["bot-token"])
    bot.sendMessage(item["telegram"]["chat_id"], overviewCopy)
