from telebot import TeleBot

from credits import bot_token
from secrets import tg_id

from base import randomizer, get_by_id, get_all_user_id, delete_user_from_db, add_user_to_db
from exceptions import UserAlreadyExistsError, UserNotExistsError


bot = TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, это бот для Тайного Санты 🎅🏼. "
                                      "Если ты хочешь поучаствовать нажми /register, чтобы зарегестрироваться в игру. "
                                      "До 10 декабря ты можешь передумать и удалиться из игры нажав /delete."
                                      "Имя человека, для которого ты должен приготовить подарок, я пришлю тебе 10 декабря."
                                      "В качестве подарка может быть что угодно, стоимостью до 5к драм:)"
                                      "Пожалуйста, не удаляйся из игры, после 10 декабря, иначе твой подопечный останется без подарка 😞"
                                      "Подарками меняемся 26 декабря!",
                     )


@bot.message_handler(commands=["register"])
def register_to_db(message):
    inf = bot.get_chat_member(message.chat.id, message.from_user.id)
    full_name = f"{inf.user.first_name} {inf.user.last_name}"
    try:
        add_user_to_db(first_name=inf.user.first_name,
                       last_name=inf.user.last_name,
                       username=inf.user.username,
                       user_id=inf.user.id)
        bot.send_message(message.chat.id, f"{full_name}, Вы успешно зарегистрированы в игру!")
    except UserAlreadyExistsError:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")


@bot.message_handler(commands=["delete"])
def delete_user_from_game(message):
    inf = bot.get_chat_member(message.chat.id, message.from_user.id)
    try:
        delete_user_from_db(inf.user.id)
        bot.send_message(message.chat.id, "Вы успешно удалены из игры!")
    except UserNotExistsError:
        bot.send_message(message.chat.id, "Вы еще не зарегестрированы!")


@bot.message_handler(commands=["play"])
def start_game(message):
    inf = bot.get_chat_member(message.chat.id, message.from_user.id)
    if inf.user.id == tg_id:
        randomizer()
        list_id = get_all_user_id()
        for id_ in list_id:
            user = get_by_id(id_)
            partner = get_by_id(user.partner_id)
            link_telegram = f"https://t.me/{partner.username}"
            bot.send_message(user.user_id, f"Твой подопечный {link_telegram}")
    else:
        bot.send_message(message.chat.id, "Нет доступа для этой команды")


bot.polling(none_stop=True)
