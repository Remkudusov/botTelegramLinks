import telebot
from telebot import types
from SQLiter import SQLiter
import link
# token = "907864815:AAHBusZIeUgs5rhBI8QN_atyQPpW3aOwszo"
token = "1148719984:AAHakavHHoj_bL1G0bDxuz8pcXVNzjyvoro"

bot = telebot.TeleBot(token)
links = []
params = []

@bot.message_handler(commands=['start'])
def startWork(message):
    code = bot.send_message(message.chat.id, 'Введите код', reply_markup = types.ReplyKeyboardRemove())
    bot.register_next_step_handler(code, startWork1)

def startWork1(message):
    code = message.text
    if str(code) == "0987654321":
        keyboard = types.ReplyKeyboardMarkup()
        createLinkButton = types.KeyboardButton('Создать ссылку')
        getLinksButton = types.KeyboardButton('Просмотреть все ссылки')
        exitButton = types.KeyboardButton('Выход')

        keyboard.add(createLinkButton)
        keyboard.add(getLinksButton)
        keyboard.add(exitButton)
        ans1 = bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)
        bot.register_next_step_handler(ans1, work)
    else:
        code = message
        status = ['creator', 'administrator', 'member']

        db_worker = SQLiter('codes.db')
        for i in range(db_worker.count_rows()):
            answer = db_worker.select_single(i)
            db_worker.connect.commit()
            if code == str(answer[0]):
                follower = False
                for j in status:
                    if bot.get_chat_member(chat_id=answer[2], user_id=message.from_user.id).status == j:
                        bot.send_message(message.chat.id, answer[4])
                        follower += 1
                if not follower:
                    bot.send_message(message.chat.id, answer[3])

        db_worker.close()
        startWork(message)

def work(message):
    if message.text == 'Создать ссылку':
        botLinkCreate(message)
    elif message.text == 'Просмотреть все ссылки':
        botWatchLink(message)
    elif message.text == 'Выход':
        bot.register_next_step_handler('/start', startWork)

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