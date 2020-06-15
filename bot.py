import telebot
from telebot import types
import logging
import datetime
import config

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.

bot = telebot.TeleBot(config.token)

### Функция проверки авторизации
# def autor(chatid):
#    strid = str(chatid)
#    for item in config.users:
#        if item == strid:
#            return True
#    return False

### Функция массвой рассылки уведомлений
#def sendall(text):
#    if len(config.users) > 0:
#        for user in config.users:
#            try:
#                bot.send_message(user, text)
#            except:
#                print(str(datetime.datetime.now()) + ' ' + 'Ошибка отправки сообщения ' + text + ' пользователю ' + str(
#                    user))

### Функция проверки режима
#def checkmode():
#    try:
#        mode_file = open("mode.txt", "r")
#        modestring = mode_file.read()
#        mode_file.close()
#        if modestring == '1':
#            return True
#        else:
#            return False
#    except:
#        return False

print(str(datetime.datetime.now()) + ' ' + 'Bot has woke up!')

### Главное меню
@bot.message_handler(commands=['Меню', 'start', 'Обновить'])
def menu(message):
    if autor(message.chat.id):
        markup = types.ReplyKeyboardMarkup()
        markup.row('/Обновить', '/Охрана')
        if checkmode():
            bot.send_message(message.chat.id, 'Режим охраны ВКЛ.', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Режим охраны ВЫКЛ.', reply_markup=markup)
        try:
            f = open(config.lastimage, 'rb')
            bot.send_photo(message.chat.id, f)
        except:
            bot.send_message(message.chat.id, 'Фоток нет')
    else:
        markup = types.ReplyKeyboardMarkup()
        markup.row('/Обновить')
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id), reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=10)
