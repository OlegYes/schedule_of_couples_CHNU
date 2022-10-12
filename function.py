import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import configparser
from fake_useragent import UserAgent
import json

def get_institute():
    data = {}
    url = "https://teach.cdu.edu.ua/cnuteach/schedule/"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="entry clr")
    element_block = block.find_all("a")
    #print(element_block)
    index = 0
    for el in element_block:
        linc = el.get("href")
        text = str(el.text).replace(u"\xa0", " ").strip()
        # print(text)
        index += 1
        data[text] = {}
        data[text]["title"] = text
        data[text]["url"] = linc
    with open("data_file.json", "w", encoding="UTF-8") as write_file:
        json.dump(data, write_file, indent=4)


def get_department():
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    d = data.keys()
    for item in d:
        if item == "ННЦ “Медичний інститут Черкаського національного університету імені Богдана Хмельницького”":
            break
        #print(item)
        linc = data[item]["url"]
        #print(linc)
        response = requests.get(linc).text
        soup = BeautifulSoup(response, "lxml")
        block = soup.find("div", class_="elementor-column-wrap elementor-element-populated")
        element_block = block.find_all("a")
        # print(element_block)
        element_block_linc = block.find_all("iframe")
        #print(element_block_linc)
        # print(element_block)
        data[item]["department"] = {}
        for el in range(len(element_block_linc)):
            el_block = element_block[el].text
            el_linc = element_block_linc[el].get("src")
            if "preview" in el_linc:
                linc_cleen = el_linc.split("preview")
            if "pubhtml" in el_linc:
                linc_cleen = el_linc.split("pubhtml")
            linces = linc_cleen[0]
            # url = el_bl.get('src')
            data[item]["department"][el_block] = {}
            data[item]["department"][el_block]["title"] = el_block
            data[item]["department"][el_block]["url"] = linces
    with open("data_file.json", "w", encoding="UTF-8") as write_file:
        json.dump(data, write_file, indent=4)


def get_timetable_foreign_languages():
    with open("data_file.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    print(data)
    d = 'ННІ іноземних мов'
    keys = data[d]['department'].keys()
    for i in keys:
        linc_dirty = data[d]['department'][i]["url"]
        #print(i, linc_dirty)

if __name__ == '__main__':
    #get_institute()
    #get_department()
    get_timetable_foreign_languages()
