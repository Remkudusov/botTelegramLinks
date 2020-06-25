import telebot
from telebot import types
import link
from SQLiter import SQLiter

# token = '1257991571:AAEsiyVd30VuM7B6wZeva6lpiaLqoroFxCg'
token = '1101844112:AAE9CdQfwr_QdveeQYvrgrUhH_6Kjbeyh10'

bot = telebot.TeleBot(token)
links = []
params = []

@bot.message_handler(commands=['start'])
def startWork(message):
    keyboard = types.ReplyKeyboardMarkup()
    createLinkButton = types.KeyboardButton('Создать ссылку')
    getLinksButton = types.KeyboardButton('Просмотреть все ссылки')

    keyboard.add(createLinkButton)
    keyboard.add(getLinksButton)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def work(message):
    if message.text == 'Создать ссылку':
        botLinkCreate(message)
    elif message.text == 'Просмотреть все ссылки':
        botWatchLink(message)

def botLinkCreate(message):
    code1 = bot.send_message(message.chat.id, 'Напишите цифру, которую должен будет ввести пользователь для того, чтобы получить ссылку', reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(code1, botCreateLinkStep1)

def botCreateLinkStep1(message):
    reply_markup = types.ReplyKeyboardRemove()
    params.append(message.text)
    channelLink1 = bot.send_message(message.chat.id, 'Введите id канала c знаком @ в начале, на который должен быть подписан пользователь, например @channel', reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(channelLink1, botCreateLinkStep2)

def botCreateLinkStep2(message):
    params.append(message.text)
    notSub1 = bot.send_message(message.chat.id, '❌ Введите сообщение, которое должен получить пользователь если он не подписан на канал', reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(notSub1, botCreateLinkStep3)

def botCreateLinkStep3(message):
    params.append(message.text)
    sub1 = bot.send_message(message.chat.id, '✔ Введите сообщение, которое должен получить пользователь если он подписан на канал', reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(sub1, botCreateLinkStep4)

def botCreateLinkStep4(message):
    params.append(message.text)
    parametr = link.Link(params[0], params[1], params[2], params[3])
    db_worker = SQLiter('codes.db')
    db_worker.insert_row(message.from_user.id, parametr.getCode(), parametr.getChannelLink(), parametr.getNotSub(), parametr.getSub())
    db_worker.connection.commit()
    db_worker.close()
    links.append(link.Link(params[0], params[1], params[2], params[3]))
    startWork(message)

def botWatchLink(message):
    db_worker = SQLiter('codes.db')
    for i in range(db_worker.count_rows()):
        answer = db_worker.select_single(i)
        result = ""
        for j in answer:
            result += str(j) + " "
        bot.send_message(message.chat.id, result, reply_markup = types.ReplyKeyboardRemove())
    db_worker.connection.commit()
    db_worker.close()
    startWork(message)

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)