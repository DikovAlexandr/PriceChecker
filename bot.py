import telebot
from telebot import types
import pandas as pd
import checker
import threading
import time
import csv

TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(TOKEN)

user_data = {}

auto_checking = threading.Event()
auto_checking.clear()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    send_menu(message)

# Menu bar
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True) #  one_time_keyboard=True
    markup.add(types.KeyboardButton("Добавить товар"))
    markup.add(types.KeyboardButton("Задать период проверки"))
    markup.add(types.KeyboardButton("Остановить автопроверку"))
    markup.add(types.KeyboardButton("Проверить сейчас"))
    markup.add(types.KeyboardButton("Очистить записи"))
    markup.add(types.KeyboardButton("Все записи"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Messang proccessor
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text == "Добавить товар":
        bot.send_message(chat_id, "Введите id товара:")
        bot.register_next_step_handler(message, process_id_step)

    elif message.text == "Задать период проверки":
        bot.send_message(chat_id, "Введите период проверки (в секундах):")
        bot.register_next_step_handler(message, process_period_step)

    elif message.text == "Остановить автопроверку":
        stop_auto_checking(message)

    elif message.text == "Проверить сейчас":
        check_prices(user_id)

    elif message.text == "Очистить записи":
        if user_id in user_data:
            user_data.pop(user_id)
        bot.send_message(chat_id, "Записи очищены.")

    elif message.text == "Все записи":
        if user_id in user_data and len(user_data[user_id]) > 0:
            records = user_data[user_id]
            response = "\n".join([f"id: {id}, target_price: {records[id]}" for id in records])
            bot.send_message(chat_id, f"Ваши записи:\n" + response)
        else:
            bot.send_message(chat_id, "У вас нет записей.")

    else:
        bot.send_message(chat_id, "Неверная команда. Выберите действие из меню.")

# Article inputting processor
def process_id_step(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        id = int(message.text)
        bot.send_message(chat_id, "Введите желаемую цену товара:")
        # If dict for user already exist
        if user_id in user_data:
            user_data[user_id][id] = None
        else:
            # If dict not exist
            user_data[user_id] = {id: None}
        bot.register_next_step_handler(message, lambda m: process_target_price_step(m, id))
    except ValueError:
        bot.send_message(chat_id, "Неверный id товара. Введите id заново.")

# Target price processor
def process_target_price_step(message, id):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        target_price = float(message.text)
        user_data[user_id][id] = target_price
        bot.send_message(chat_id, f"Запись добавлена: артикул {id}, цена={target_price}")
    except ValueError:
        bot.send_message(chat_id, "Неверная цена. Введите цену заново.")

# Automatic checker
def process_period_step(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try: 
        period = int(message.text)
        bot.send_message(chat_id, f"Период проверки установлен: {period} секунд.")

        global auto_checking
        auto_checking.set()
        threading.Thread(target=schedule_check_prices, args=(period, user_id,), daemon=True).start()
    except ValueError:
        bot.send_message(chat_id, "Неверный период. Введите период заново.")

# Automatic price checker start
def schedule_check_prices(period, user_id):
    global auto_checking
    
    while auto_checking.is_set():
        check_prices(user_id)
        time.sleep(period)

# Automatic price checker stop
def stop_auto_checking(message):    
    user_id = message.from_user.id
    chat_id = message.chat.id

    global auto_checking
    auto_checking.clear()
    bot.send_message(chat_id, "Автоматическая проверка выключена.")

# Check prices for all products
def check_prices(user_id):
    result = ""
    if user_id in user_data:
        ids = []
        target_prices= []
        for id in user_data[user_id]:
            ids.append(id)
            target_prices.append(user_data[user_id][id])
        best_price_ids = checker.process(ids, target_prices)
        if best_price_ids:
            print("Best Price :", best_price_ids)
            for id in best_price_ids:
                result += f"Товар {id} соответствует желаемой стоимости\n"
                bot.send_message(user_id, result)
        # else: 
        #     result = f"Таких товаров нет, код проверки вернул {best_price_ids}"
        #     bot.send_message(user_id, result)


if __name__ == '__main__':
    bot.polling(none_stop=True)
