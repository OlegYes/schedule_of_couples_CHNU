import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import configparser
import json

# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

bot_key = config['Telegram']['token']
linc = "https://teach.cdu.edu.ua/cnuteach/schedule/"

bot = telebot.TeleBot(bot_key, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
data = {"chat_id": {"institute": None,"course": None, "course_linc": [], "linc": None}, "institute_linc": []}
#jdata = json.load(data)

def myfu():
    pass
    # with open('index.html', 'w') as f:
    #     data = block
    #     f.write(data.text)


@bot.message_handler(commands=['start'])
def institute(message):
    if str(message.chat.id) in data:
        data.pop(str(message.chat.id))
    #print(data["chat_id"])
    data.setdefault(str(message.chat.id), {"institute": None, "course": None, "course_linc": [], "linc": None})
    #print(data)
    #print(data[str(message.chat.id)]["institute"])
    response = requests.get(linc).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="entry clr")
    element_block = block.find_all("a")
    # print(element_block)

    index = 0
    buttons = []
    markup = types.InlineKeyboardMarkup()
    for el in element_block:
        url = el.get('href')
        data["institute_linc"].append(str(url))
        krakozabra = str(el.text)
        button = types.InlineKeyboardButton(krakozabra, callback_data=str(index))
        index += 1
        markup.row(button)
        #print(markup)

    bot.send_message(message.chat.id, 'Оберіть інститут', reply_markup=markup)




def course(call, linc):
    #bot.reply_to(message, "Howdy, how are you doing?")
    markup = types.InlineKeyboardMarkup()
    pre_linc = data.get(str(call.message.chat.id))
    print(linc)
    response = requests.get(linc).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="elementor-column-wrap elementor-element-populated")
    element_block = block.find_all("a")
    # print(element_block)
    for el in element_block:
        button = types.InlineKeyboardButton(el.text, callback_data=el.text)
        markup.row(button)
        print(markup)
    bot.send_message(call.message.chat.id, 'Оберіть курс', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if data[str(call.message.chat.id)]["institute"] == None:
        data[str(call.message.chat.id)]["institute"] = call.data
        linc = data["institute_linc"][int(call.data)]
        #print(linc)
        course(call, linc)
    if data[str(call.message.chat.id)]["institute"] != None:
        if data[str(call.message.chat.id)]["course"] == None:
            data[str(call.message.chat.id)]["course"] = call


    # bot.send_message(call.message.chat.id, ' {}'.format(str(call.data)))
    # bot.answer_callback_query(call.id)


if __name__ == '__main__':
    bot.infinity_polling()
    #myfu()



