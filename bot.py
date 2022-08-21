import config
import telebot
import random
import requests
from bs4 import BeautifulSoup as b
from telebot import types

URL = 'https://world-weather.ru/pogoda/russia/moscow/7days/'
r = requests.get(URL)
soup = b(r.text, 'html.parser')
weather = soup.find_all('div', id = "weather-now-number")
clear_weather = [c.text for c in weather]


bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def hi(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}'
                                      f'\nУзнать возможности бота - /help')

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Рандомное число')
    item2 = types.KeyboardButton('Погода')
    item3 = types.KeyboardButton('id')
    item4 = types.KeyboardButton('Купить телефон')
    item5 = types.KeyboardButton('Да/Нет')
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Открылось меню',reply_markup = markup)


@bot.message_handler(content_types=['text', 'photo'])
def echo_all(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,f'Привет, {message.from_user.first_name} {message.from_user.last_name}'
                                      f'\nУзнать возможности бота - /help')
    elif message.text == 'Рандомное число':
        bot.send_message(message.chat.id, f'Ваше число: {random.randint(0,1000)}')
    elif message.text == 'id':
        bot.send_message(message.chat.id, f'Твой id: {message.from_user.id}')
    elif message.text == 'Погода':
        bot.send_message(message.chat.id, f'Погода в москве: {clear_weather[0]}')
    elif message.text == 'Купить телефон':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Iphone')
        item2 = types.KeyboardButton('Samsung')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Выбор телефона', reply_markup=markup)
    elif message.text == 'Samsung':
        mark = types.InlineKeyboardMarkup(row_width=1)
        item2 = types.InlineKeyboardButton('Samsung link', url='https://www.samsung.com/ru/')
        mark.add(item2)
        bot.send_message(message.chat.id, 'Перейти на сайт Самсунг', reply_markup=mark)
    elif message.text == 'Iphone':
        url2 = 'https://telemarket24.ru/catalog/apple_iphone/'
        p = requests.get(url2)
        soup = b(p.text, 'html.parser')
        iphone = soup.find_all('div', class_='catalog blocks active')
        for products in iphone:
            product_iphone = products('div', class_='catalog-item tovar_inner blocks-item wow fadeIn')
            for name in product_iphone:
                name_iphone = name.find('span', class_='text').get_text(strip=True)
                price_iphone = name.find('span', class_='value').get_text(strip=True)
                link_iphone = name.find('a').get('href')
                all_prod = f'{name_iphone} \n{price_iphone} Рублей \nhttps://telemarket24.ru{link_iphone}'
                bot.send_message(message.chat.id, all_prod)
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Рандомное число')
        item2 = types.KeyboardButton('Погода')
        item3 = types.KeyboardButton('id')
        item4 = types.KeyboardButton('Купить телефон')
        item5 = types.KeyboardButton('Да/Нет')
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)
    elif message.text == 'Да/Нет':
        yes_or_not = random.randint(1, 2)
        if yes_or_not == 1:
            bot.send_message(message.chat.id, 'Да')
        else:
            bot.send_message(message.chat.id, 'Нет')

    else:
        bot.send_photo(message.chat.id, open('mem.jpg', 'rb'))

bot.polling(none_stop=True)
