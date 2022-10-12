import fake_useragent
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import configparser
from fake_useragent import UserAgent

# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

bot_key = config['Telegram']['token']
linc = "https://teach.cdu.edu.ua/cnuteach/schedule/"

bot = telebot.TeleBot(bot_key, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
data = {"chat_id": {"institute": None, "course": None, "group": None, "sabgroup": None,"my_course": None, "my_group": None,"my_sabgroup": None, "pair": [], "course_linc": [], "linc": None}, "institute_linc": []}
#jdata = json.load(data)


def get_institute():
    url = "https://teach.cdu.edu.ua/cnuteach/schedule/"
    response = requests.get(linc).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="entry clr")
    element_block = block.find_all("a")
    # print(element_block)
    index = 0
    for el in element_block:
        index += 1

def parser():
    pass


def parser_IOTEX_phis(call, linc_dirty):
    #linc_dirty = "https://docs.google.com/spreadsheets/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/preview;single=true&widget=true&headers=false#gid=1601027181"
    #linc = "https://docs.google.com/spreadsheets/u/0/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/preview/sheet?gid=1601027181"
    #linc = "https://docs.google.com/spreadsheets/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/"
    #linc = "https://teach.cdu.edu.ua/cnuteach/schedule/it/"
    if "preview" in linc_dirty:
        linc_cleen = linc_dirty.split("preview")
    if "pubhtml" in linc_dirty:
        linc_cleen = linc_dirty.split("pubhtml")
    linc = linc_cleen[0]
    response = requests.get(linc).text
    #print(response)
    soup = BeautifulSoup(response, "lxml")
    day_week = soup.find("td", class_="s0").text
    groups_IOTEX = soup.find_all("td", class_="s2")
    groups_IOTEX_list = []
    for el in groups_IOTEX:
        colspan = el.get("colspan")
        if colspan != None:
            for i in range(int(colspan)):
                groups_IOTEX_list.append(el.text)

                if el.text == "IV-І":
                    g = soup.find_all("td", class_="s3")
                    for j in g:
                        groups_IOTEX_list.append(j.text)
                #print(groups_IOTEX_list)
        else:
            groups_IOTEX_list.append(el.text)
            grupa = el.text
            if el.text == "IV-І":
                g = soup.find_all("td", class_="s3")
                for j in g:
                    groups_IOTEX_list.append(j.text)
            #print(groups_IOTEX_list)
    sabgroup = soup.find_all("td", class_="s5")
    sabgroup_list = []
    for el in sabgroup:
        colspan = el.get("colspan")
        if colspan != None:
            for i in range(int(colspan)):
                sabgroup_list.append(el.text)
                # print(sabgroup_list)

        else:
            sabgroup_list.append(el.text)
            # print(sabgroup_list)
    # print(len(sabgroup_list))
    # print(len(groups_IOTEX_list))
    par = soup.find_all("td", class_="s7")
    par_list = []
    first_pair = []
    second_pair = []
    third_pair = []
    fourth_pair = []
    fifth_pair = []
    sixth_pair = []
    seventh_pair = []

    iterat = 0
    max_iterat = len(groups_IOTEX_list)
    for el in par:
        colspan = el.get("colspan")
        if colspan != None:
            for i in range(int(colspan)):
                par_list.append(el.text)
                # print(sabgroup_list)
                iterat += 1
        else:
                par_list.append(el.text)
                iterat += 1
    first_pair = par_list[:len(groups_IOTEX_list)]
    second_pair = par_list[len(groups_IOTEX_list):2*len(groups_IOTEX_list)]
    third_pair = par_list[2*len(groups_IOTEX_list):3*len(groups_IOTEX_list)]
    fourth_pair = par_list[3*len(groups_IOTEX_list):4*len(groups_IOTEX_list)]
    fifth_pair = par_list[4*len(groups_IOTEX_list):5*len(groups_IOTEX_list)]
    sixth_pair = par_list[5*len(groups_IOTEX_list):6*len(groups_IOTEX_list)]
    seventh_pair = par_list[6*len(groups_IOTEX_list):7*len(groups_IOTEX_list)]

    data[str(call.message.chat.id)]["group"] = groups_IOTEX_list
    data[str(call.message.chat.id)]["sabgroup"] = sabgroup_list
    data[str(call.message.chat.id)]["pair"] = [first_pair, second_pair, third_pair, fourth_pair, fifth_pair, sixth_pair, seventh_pair]
    # print(first_pair)
    # print(second_pair)
    # print(third_pair)
    # print(fourth_pair)
        #bot.send_message(message.chat.id, 'Оберіть інститут', reply_markup=markup)
    # with open('index.html', 'w') as f:
    #     data = str(groups)
    #     f.write(data)


@bot.message_handler(commands=['start'])
def institute(message):
    if str(message.chat.id) in data:
        data.pop(str(message.chat.id), {"institute": None, "course": None, "group": None, "sabgroup": None,"my_course": None, "my_group": None,"my_sabgroup": None, "pair": [], "course_linc": [], "linc": None})
    #print(data["chat_id"])
    data.setdefault(str(message.chat.id), {"institute": None, "course": None, "group": None, "sabgroup": None,"my_course": None, "my_group": None,"my_sabgroup": None, "pair": [], "course_linc": [], "linc": None})
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
        print(krakozabra)
        button = types.InlineKeyboardButton(krakozabra, callback_data=str(index))
        index += 1
        markup.row(button)

        #print(markup)

    bot.send_message(message.chat.id, 'Оберіть інститут', reply_markup=markup)




def course(call, linc):
    global data
    #bot.reply_to(message, "Howdy, how are you doing?")
    markup = types.InlineKeyboardMarkup()
    response = requests.get(linc).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="elementor-column-wrap elementor-element-populated")
    element_block = block.find_all("a")
    # print(element_block)
    element_block_linc = block.find_all("iframe")
    # print(element_block_linc)
    # print(element_block)
    for el in element_block_linc:
        url = el.get('src')
        data[str(call.message.chat.id)]["course_linc"].append(str(url))
        # print(data)
    iterat = 0
    # with open('cours_linc.txt', 'w') as f:
    #     data = str(data[str(call.message.chat.id)]["course_linc"])
    #     f.write(data)

    for el in element_block:
        button = types.InlineKeyboardButton(el.text, callback_data=str(iterat))
        iterat += 1
        markup.row(button)
        #print(markup)
    bot.send_message(call.message.chat.id, 'Оберіть курс', reply_markup=markup)



def group(call, linc):
    markup = types.InlineKeyboardMarkup()
    if int(call.data) == 0:
        parser_IOTEX_phis(call, linc)

    iterat = 0
    for el in data[str(call.message.chat.id)]["group"]:
        print(f"""{el}, {data[str(call.message.chat.id)]["sabgroup"][iterat]}""")
        message = f"""{el}, {data[str(call.message.chat.id)]["sabgroup"][iterat]}"""
        button = types.InlineKeyboardButton(message, callback_data=str(iterat))
        markup.row(button)
        iterat += 1
    bot.send_message(call.message.chat.id, 'Оберіть групу', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    global data
    if data[str(call.message.chat.id)]["institute"] != None:
        print(data[str(call.message.chat.id)])
        if data[str(call.message.chat.id)]["my_course"] != None:
            if data[str(call.message.chat.id)]["my_group"] == None:
                # data[str(call.message.chat.id)]["pair"] = [first_pair, second_pair, third_pair, fourth_pair, fifth_pair,
                #                                            sixth_pair, seventh_pair]
                #
                print(call.data)
                message = f"""{data[str(call.message.chat.id)]["group"][int(call.data)]}
                1: {data[str(call.message.chat.id)]["pair"][0][int(call.data)]}\n
                2: {data[str(call.message.chat.id)]["pair"][1][int(call.data)]}\n
                3: {data[str(call.message.chat.id)]["pair"][2][int(call.data)]}\n
                4: {data[str(call.message.chat.id)]["pair"][3][int(call.data)]}\n
                5: {data[str(call.message.chat.id)]["pair"][4][int(call.data)]}\n
                6: {data[str(call.message.chat.id)]["pair"][5][int(call.data)]}\n
                7: {data[str(call.message.chat.id)]["pair"][6][int(call.data)]}\n           
                            """
                bot.send_message(call.message.chat.id, message)



    if data[str(call.message.chat.id)]["institute"] != None:
        if data[str(call.message.chat.id)]["my_course"] == None:
            print(call.data)
            data[str(call.message.chat.id)]["my_course"] = call
            linc = data[str(call.message.chat.id)]["course_linc"][int(call.data)]
            group(call, linc)
    if data[str(call.message.chat.id)]["institute"] == None:
        print(True)
        data[str(call.message.chat.id)]["institute"] = call.data
        linc = data["institute_linc"][int(call.data)]
        #print(linc)
        course(call, linc)



    # bot.send_message(call.message.chat.id, ' {}'.format(str(call.data)))
    # bot.answer_callback_query(call.id)


if __name__ == '__main__':


    bot.infinity_polling()
    #parser_IOTEX_phis()
    #myfu()



