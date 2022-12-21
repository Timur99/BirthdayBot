import schedule
import time
import telebot
from threading import Thread
from telebot.apihelper import ApiTelegramException

# основнйо бот
bot = telebot.TeleBot("5841618545:AAEd-BRsbCak65TAUGSYvGYJ6yiW_YD8Nik")

join_file = open("join.txt")
join_users = set()
for line in join_file:
    join_users.add(line.strip())
join_file.close()


@bot.message_handler(commands=["start"])
def startjoin(message):
    join_file = open("join.txt", "a")
    join_file.write(str(message.chat.id) + "/n")
    join_users.add(message.chat.id)


@bot.message_handler(commands=["send"])
def mess(message):
    for user in join_users.copy():
        try:
            bot.send_message(user, message.text[message.text.find(' '):])
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(message.chat.id))


def sheduler():
    schedule.every().day.at("22:00").do(daily_notify)

    while True:
        schedule.run_pending()
        time.sleep(1)


def daily_notify():
    for user in join_users:
        try:
            bot.send_message(user, "С днем рождения. Прости нас")
            bot.send_message(user, "Туган көнең белән сине")
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(user))


def main_loop():
    thread = Thread(target=sheduler)
    thread.start()

    bot.polling(True)

if __name__ == '__main__':
    main_loop()

