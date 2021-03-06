from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


class KTM:

    PAGE_LOGIN = "https://billing.alexandriya.net:9443/index.cgi"
    PAGE_OVERVIEW = "https://billing.alexandriya.net:9443/index.cgi"

    def __init__(self, options):
        self.username = options.get("username") or ""
        self.password = options.get("password") or ""
        self.debug = options.get("debug") or False
        options = ChromeOptions()
        if not self.debug:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            options=options
        )

    def __login(self):
        try:
            self.driver.get(self.PAGE_LOGIN)
            self.driver.execute_script(f'''
                document.querySelector("#user").value = "{self.username}";
                document.querySelector("#passwd").value = "{self.password}";
                document.querySelector("[name=logined]").click();
            ''')
            return True
        except:
            return False

    def __logout(self):
        try:
            self.driver.execute_script(f'''
                document.querySelector("#logout").click()
            ''')
            self.driver.quit()
            return True
        except:
            return False

    def __overview(self):
        overview = {}
        # balance
        try:
            overview['balance'] = self.driver.execute_script(f'''
                var $el = document.querySelector("#main-content > div.row > div:nth-child(4) > div > div.card-body.p-2 > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div:nth-child(1)")
                var balance = parseFloat($el.textContent.trim())
                return isNaN(balance) ? null : balance;
            ''')
        except:
            overview['balance'] = None
        # rate, message_end, cost, mac, speed
        try:
            items = self.driver.execute_script('''
                var $el = document.querySelector("#main-content > div.card.card-primary.card-outline > div.card-body")
                var items = $el.innerText.split("\\n")
                return {
                    rate: items[0],
                    message_end: items[1],
                    cost: parseFloat(items[8].split("\\t")[1]),
                    mac: items[12].split("\\t")[1],
                    speed: items[13],
                }
            ''')
            for k in items:
                overview[k] = items[k]
        except:
            pass
        return overview

    def getOverview(self):
        self.__login()
        overview = self.__overview()
        self.__logout()
        return overview

    def getOverviewTest(self):
        return {
            'balance': 123.45,
            'cost': 80,
            'mac': '00:22:15:e0:dd:41',
            'message_end': '???????????? ???????????????????? ?????????? 50 ????????. (2021-10-17)',
            'rate': 'middle',
            'speed': '50 mbps'
        }
