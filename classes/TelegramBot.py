import telebot


class TelegramBot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode="HTML")

    def sendMessage(self, chatID, overview):
        try:
            self.bot.send_message(chatID, "\n".join([
                "<b>{}</b>".format(overview["username"]),
                "\U0001F4B5 <b>{:.2f}</b> грн ({:.2f} грн)".format(overview["balance"], -overview["diff"]),
                "\U0001F4F6 {} {}, {} грн".format(overview["rate"], overview["speed"], overview["cost"]),
                "{}".format(overview["message_end"]),
            ]))
            return True
        except Exception as e:
            print(e)
            return False
