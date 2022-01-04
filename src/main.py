import telebot
from telebot import types, custom_filters

from settings import ADMINS, TELEGRAM_TOKEN, SMTP
from messages import is_correct_mail

bot = telebot.TeleBot(TELEGRAM_TOKEN)


# states

class States:
    ask_mail = 1
    ask_password = 2
    ask_name = 3
    ask_link = 4
    complete = 5
    change_name = 6
    change_link = 7
    change_work = 8
    change_about = 9

# general functions


def help(message):
    user_id = message.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    keyboard.add(
        types.InlineKeyboardButton(
            text='Посмотреть свой профиль',
            callback_data='show_profile'
        ),
        types.InlineKeyboardButton(
            text='Поменять данные профиля',
            callback_data='change_profile'
        ),
        types.InlineKeyboardButton(
            text='Поставить на паузу',
            callback_data='set_pause'
        ),
        types.InlineKeyboardButton(
            text='Снять паузу',
            callback_data='set_run'
        )
    )

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, 'Выбери подходящую опцию ниже', reply_markup=keyboard)

# user commands


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_mail

    answer = ('Привет!🤩\n'
              'Я Random Coffee бот 🤖\n\n'
              'Каждую неделю я буду предлагать '
              'тебе для встречи интересного человека, '
              'случайно выбранного среди '
              'других участников🎲\n\n'
              'Введи свой корпоративный mail, '
              'чтобы получить пароль📧')

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.ask_mail)
def ask_mail_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_password

    mail = message.text

    if is_correct_mail(mail) and SMTP:
        answer = ('Отправил📮\n'
                  'Введи пароль из письма🔑')
    elif is_correct_mail(mail) and not SMTP:
        answer = ('Напиши админу, '
                  f'чтобы получить пароль ({", ".join(ADMINS)})🛡️'
                  'И введи его сюда🔑')
    else:
        answer = ('Введи свой корпоративный mail, '
                  'чтобы получить пароль📧')
        next_state = States.ask_mail

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.ask_password)
def ask_password_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_name

    answer = ('Ты в системе🌐\n\n'
              'Как тебя зовут?☕️')

    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.ask_name)
def ask_name_handler(message):
    user_id = message.from_user.id
    next_state = States.ask_link

    answer = ('Рад познакомиться!)\n\n'
              'Пришли ссылку на свой профиль '
              'в любой социальной сети. '
              'Так вы в паре сможете лучше узнать '
              'друг о друге до встречи🔎')

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.ask_link)
def ask_link_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    answer = ('Отлично, все готово!✨\n\n'
              'Свою пару для встречи ты будешь узнавать'
              ' каждый понедельник — сообщение придет в этот чат\n\n'
              'Напиши партнеру в Telegram, '
              'чтобы договориться о встрече или звонке\n'
              'Время и место вы выбираете сами\n\n'
              'Если остались вопросы - /help!)')

    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer)
    bot.set_state(user_id, next_state)


@bot.message_handler(commands=['help'], state=[States.complete, ])
def help_handler(message):
    help(message)


@bot.message_handler(state=States.change_name)
def change_name_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    answer = 'Готово'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_link)
def change_link_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    answer = 'Готово'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_work)
def change_work_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    answer = 'Готово'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.message_handler(state=States.change_about)
def change_about_handler(message):
    user_id = message.from_user.id
    next_state = States.complete

    answer = 'Готово'

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)

# user callbacks


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = call.message.text

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    help(call)


@bot.callback_query_handler(func=lambda call: call.data == 'show_profile')
def show_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = ('👉 Хочу посмотреть свой профиль')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = (
        'Вот так будет выглядеть твой профиль для собеседника:\n\n'
        'Иван Иванов\n'
        '*Профиль:* t.me\n\n'
        '*Чем занимается:* Python Developer\n'
        '*Зацепки для начала разговора:* Meow',
    )

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, parse_mode='Markdown', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'change_name')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_name

    answer = ('👉 Своё имя')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Введи свое имя')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_link')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_link

    answer = ('👉 Ссылку на социальную сеть')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Введи новую ссылку')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_work')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_work

    answer = ('👉 Кем работаю')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Напиши, чем ты занимаешься по работе')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_about')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.change_about

    answer = ('👉 О себе')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Напиши  новое описание:'
              ' пара предложений о твоих профессиональных'
              ' интересах, взглядах, хобби')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'change_profile')
def change_profile_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    next_state = States.complete

    answer = ('👉 Поменять данные профиля')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Что хочешь поменять?')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1

    keyboard.add(
        types.InlineKeyboardButton(
            text='Своё имя',
            callback_data='change_name'
        ),
        types.InlineKeyboardButton(
            text='Ссылку на социальную сеть',
            callback_data='change_link'
        ),
        types.InlineKeyboardButton(
            text='Кем работаю',
            callback_data='change_work'
        ),
        types.InlineKeyboardButton(
            text='О себе',
            callback_data='change_about'
        ),
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)
    bot.set_state(user_id, next_state)


@bot.callback_query_handler(func=lambda call: call.data == 'set_pause')
def set_pause_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = ('👉 Поставить на паузу')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Готово')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'set_run')
def set_run_callback(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    answer = ('👉 Снять паузу')

    bot.send_chat_action(user_id, 'typing')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=answer
    )

    answer = ('Готово')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    )
    bot.send_chat_action(user_id, 'typing')
    bot.send_message(user_id, answer, reply_markup=keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

if __name__ == "__main__":
    bot.polling()
