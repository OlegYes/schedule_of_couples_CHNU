import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import configparser
from fake_useragent import UserAgent
import json


# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

bot_key = config['Telegram']['token']
# linc = "https://teach.cdu.edu.ua/cnuteach/schedule/"

bot = telebot.TeleBot(bot_key, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
data_user = {"chat_id": {"institute": None, "course": None, "group": None, "sabgroup": None,"my_course": None, "my_group": None,"my_sabgroup": None, "pair": [], "course_linc": [], "linc": None}, "institute_linc": []}
#jdata = json.load(data)


def get_department():
    data = {}
    #print(item)
    linc = 'https://teach.cdu.edu.ua/cnuteach/schedule/it/'
    #print(linc)
    response = requests.get(linc).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="elementor-column-wrap elementor-element-populated")
    element_block = block.find_all("a")
    # print(element_block)
    element_block_linc = block.find_all("iframe")
    #print(element_block_linc)
    # print(element_block)
    data["department"] = {}
    for el in range(len(element_block_linc)):
        el_block = element_block[el].text
        el_linc = element_block_linc[el].get("src")
        if "preview" in el_linc:
            linc_cleen = el_linc.split("preview")
        if "pubhtml" in el_linc:
            linc_cleen = el_linc.split("pubhtml")
        linces = linc_cleen[0]
        # url = el_bl.get('src')
        data["department"][el_block] = {}
        data["department"][el_block]["title"] = el_block
        data["department"][el_block]["url"] = linces
    with open("data_file.json", "w", encoding="UTF-8") as write_file:
        json.dump(data, write_file, indent=4)



def parser_IOTEX_phis():
    #linc_dirty = "https://docs.google.com/spreadsheets/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/preview;single=true&widget=true&headers=false#gid=1601027181"
    #linc = "https://docs.google.com/spreadsheets/u/0/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/preview/sheet?gid=1601027181"
    #linc = "https://docs.google.com/spreadsheets/d/1ZfpJKQoipSLkJuYFQuynASqpws1g-Bk9NPhQClv3Oz8/"
    #linc = "https://teach.cdu.edu.ua/cnuteach/schedule/it/"

    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)

    linc = data['department']['Зміни фізичне відділення']['url']
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

    data['department']['Зміни фізичне відділення']["group"] = groups_IOTEX_list
    data['department']['Зміни фізичне відділення']["sabgroup"] = sabgroup_list
    data['department']['Зміни фізичне відділення']["pair"] = [first_pair, second_pair, third_pair, fourth_pair, fifth_pair, sixth_pair, seventh_pair]
    with open("data_file.json", "w", encoding="UTF-8") as write_file:
        json.dump(data, write_file, indent=4)
    # print(second_pair)
    # print(third_pair)
    # print(fourth_pair)


def parser_IOTEX_mat():
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    #print(data['department']['Зміни математичне відділення'])
    linc = data['department']['Зміни математичне відділення']['url']
    response = requests.get(linc).text
    # print(response)
    soup = BeautifulSoup(response, "lxml")
    day_week = soup.find("td", class_="s0").text
    groups_IOTEX = soup.find_all("td", class_="s2")
    groups_IOTEX_list = []
    for el in groups_IOTEX:
        print(el)
        colspan = el.get("colspan")
        if colspan != None:
            for i in range(int(colspan)):
                groups_IOTEX_list.append(el.text)
        else:
            groups_IOTEX_list.append(el.text)
            grupa = el.text
    g = soup.find_all("td", class_="s3")
    for el in g:
        colspan = el.get("colspan")
        if colspan != None:
            for i in range(int(colspan)):
                groups_IOTEX_list.append(el.text)
        else:
            groups_IOTEX_list.append(el.text)

    #print(groups_IOTEX_list)
    sabgroup = soup.find_all("td", class_="s4")
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
    print(len(sabgroup_list))
    print(len(groups_IOTEX_list))
    par = soup.find_all("td", class_="s6")
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
    second_pair = par_list[len(groups_IOTEX_list):2 * len(groups_IOTEX_list)]
    third_pair = par_list[2 * len(groups_IOTEX_list):3 * len(groups_IOTEX_list)]
    fourth_pair = par_list[3 * len(groups_IOTEX_list):4 * len(groups_IOTEX_list)]
    fifth_pair = par_list[4 * len(groups_IOTEX_list):5 * len(groups_IOTEX_list)]
    sixth_pair = par_list[5 * len(groups_IOTEX_list):6 * len(groups_IOTEX_list)]
    seventh_pair = par_list[6 * len(groups_IOTEX_list):7 * len(groups_IOTEX_list)]
    data['department']['Зміни математичне відділення']["group"] = groups_IOTEX_list
    data['department']['Зміни математичне відділення']["sabgroup"] = sabgroup_list
    data['department']['Зміни математичне відділення']["pair"] = [first_pair, second_pair, third_pair, fourth_pair,
                                                              fifth_pair, sixth_pair, seventh_pair]
    with open("data_file.json", "w", encoding="UTF-8") as write_file:
        json.dump(data, write_file, indent=4)



@bot.message_handler(commands=['time'])
def pair_time(message):
    bot.send_message(message.chat.id, '1 пара 8:00-9:20\n2 пара 9:40-11:00\n3 пара 11:20-12:40\n4 пара 13:00-14:20\n5 пара 14:40-16:00\n6 пара 16:20-17:40\n7 пара 17:50-19:10\n')



@bot.message_handler(commands=['start'])
def institute(message):
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    d = data['department'].keys()
    index = 0
    markup = types.InlineKeyboardMarkup()
    for el in d:
        krakozabra = str(data['department'][el]['title'])
        #print(krakozabra)
        button = types.InlineKeyboardButton(krakozabra.title(), callback_data=str(index))
        index += 1
        markup.row(button)

        #print(markup)

    bot.send_message(message.chat.id, 'Оберіть курс', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    #print(call.message.text)
    if call.message.text == "Оберіть курс":
        d = list(data['department'].keys())
        depo = d[int(call.data)]
        data_user[str(call.message.chat.id)] = {}
        data_user[str(call.message.chat.id)]['department'] = depo
        with open("data_file_user.json", "w", encoding="UTF-8") as write_file:
            json.dump(data_user, write_file, indent=4)
        list_group = data['department'][depo]['group']
        list_sabgroup = data['department'][depo]['sabgroup']
        #print(list_sabgroup)
        markup = types.InlineKeyboardMarkup()
        index = 0
        for i in list_group:
            print(len(list_group), len(list_sabgroup))
            text = f"{i}, {list_sabgroup[index]}"
            button = types.InlineKeyboardButton(text, callback_data=str(index))
            index += 1
            markup.row(button)
        bot.send_message(call.message.chat.id, 'Оберіть групу', reply_markup=markup)
    if call.message.text == "Оберіть групу":

        list_pars = data['department'][data_user[str(call.message.chat.id)]['department']]['pair']
        #print(list_pars)
        message = str(data_user[str(call.message.chat.id)]['department'])+f"\n{data['department'][data_user[str(call.message.chat.id)]['department']]['group'][int(call.data)]}"
        print()
        index = 7
        try:
            for i in range(7):
                index = i
                iis_work = list_pars[i][int(call.data)]

        except:
            for i in range(index-1):
                message = message+f"\nПара {i+1}: {(str(list_pars[i][int(call.data)]))}"
        print(index,message)
        bot.send_message(call.message.chat.id, message)
    # if data[str(call.message.chat.id)]["institute"] != None:
    #     if data[str(call.message.chat.id)]["my_course"] == None:
    #         print(call.data)
    #         data[str(call.message.chat.id)]["my_course"] = call
    #         linc = data[str(call.message.chat.id)]["course_linc"][int(call.data)]
    #         group(call, linc)
    # if data[str(call.message.chat.id)]["institute"] == None:
    #     print(True)
    #     data[str(call.message.chat.id)]["institute"] = call.data
    #     linc = data["institute_linc"][int(call.data)]
    #     #print(linc)
    #     course(call, linc)

if __name__ == '__main__':
    bot.infinity_polling()
    #get_department()
    #parser_IOTEX_phis()
    parser_IOTEX_mat()
    #data['department']
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    #print(call.message.text)
    d = list(data.keys())
    #print(data)

