import config
import telebot
import random
import requests
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot(config.TOKEN)
markup = telebot.types.ReplyKeyboardMarkup()
markup.row("/news")
markup.row("/job")



@bot.message_handler(commands=['help'])
def sendWelcome(message):
    # bot.send_message(message.chat.id, "")
    bot.send_message(message.chat.id, "Я умею:", reply_markup=markup)


@bot.message_handler(commands=['start'])
def sendStart(message):
    bot.send_message(message.chat.id, 'Эъэъхъ. Здарова, баклан. Я *Баттхед*', parse_mode='Markdown')
    welcome_sticker = open('temp/bh.webp', 'rb')
    bot.send_sticker(message.chat.id, welcome_sticker)
    bot.send_message(message.chat.id, 'Пиши */help*, чтобы я показал, что я умею ;)', parse_mode='Markdown')


@bot.message_handler(commands=['random'])
def sendRandomWord(message):
    dice = random.randint(0, 3)
    with open('temp/words.txt', 'r') as file:
        lines = file.readlines()
        rndword = random.choice(lines).rstrip()
    bot.send_message(message.chat.id, rndword)


@bot.message_handler(commands=['news'])
def sendNewsList(message):
    newsURL = "http://mignews.com/"
    req = requests.get(newsURL, verify=False)
    soup = bs(req.text, "html.parser")
    news = soup.find_all('div', class_='lenta')
    for i in range(len(news)):
        if news[i].find('a', class_='time2 time3') is not None or news[i].find('a', class_='time2') is not None:
            bot.send_message(message.chat.id, news[i].text)


@bot.message_handler(commands=['job'])
def sendjobs(message):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'
    }
    URL = 'https://almaty.hh.kz/search/vacancy?area=160&text=Python&page=0'
    r = requests.get(URL, headers=HEADERS, )
    soup = bs(r.text, 'html.parser')
    vacancys = soup.find_all('div', class_='vacancy-serp-item')
    #url_button = telebot.types.InlineKeyboardButton(text="Перейти к вакансии", url="")
    for vacancy in vacancys:
        name = vacancy.find('a', class_='bloko-link HH-LinkModifier').text
        link = vacancy.find('a')['href']
        money = vacancy.find('div', class_='vacancy-serp-item__sidebar').find('span', class_='bloko-section-header-3 bloko-section-header-3_lite')
        if money is not None:
            bot.send_message(message.chat.id, '*%s*  *$:* %s [%s]' % (name, money.text, link), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "*%s*  *$:* ~  [%s]" %(name, link), parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
