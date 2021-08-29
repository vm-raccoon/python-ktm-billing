from classes.Config import Config
from classes.KTM import KTM
from classes.Database import Database as DB
from datetime import date


def compareDateToday(dt):
    return date.today().strftime("%Y-%m-%d") == dt[:10]


for item in Config(__file__, "config.json").read():
    db = DB(item["sqlite"])
    lastRow = db.getLastHistoryRow()

    if compareDateToday(lastRow["datetime"]):
        continue

    ktm = KTM(item["ktm-account"])
    overview = ktm.getOverview()
    db.insert(overview)
