from classes.KTM import KTM
from classes.Config import Config


config = Config(__file__, "config.json").read()
# print(config)

for item in config:
    ktm = KTM(item["ktm-account"])
    overview = ktm.getOverview()
    print(overview)
