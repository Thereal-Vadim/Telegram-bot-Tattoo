import telebot
from telebot import types

# Инициализация бота
bot_token = 'Token'
bot = telebot.TeleBot(bot_token)

# Глобальные переменные для хранения данных клиента
client_data = {}


# Функция для создания клавиатуры с постоянной кнопкой FAQ
def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Начать опрос')
    button2 = types.KeyboardButton('FAQ')
    markup.add(button1, button2)
    return markup


# Кнопка Старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот тату-мастера. Нажмите 'Начать опрос', чтобы записаться на консультацию или 'FAQ', чтобы узнать о нас.",
                     reply_markup=create_keyboard())


# Обработка FAQ
@bot.message_handler(func=lambda message: message.text == 'FAQ')
def faq(message):
    markup = create_keyboard()
    button1 = types.KeyboardButton('Обо мне')
    button2 = types.KeyboardButton('Как подготовиться к сеансу?')
    button3 = types.KeyboardButton('Как записаться на сеанс?')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Выберите раздел FAQ:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Обо мне')
def about_me(message):
    response = ("Привет, я Карина Руни, и я тату мастер)\n"
                "Давай знакомиться!\n\n"
                "Если ты хочешь подчеркнуть красоту своего тела, то читай ниже, как будет происходить наше с тобой взаимодействие:\n\n"
                "Меня зовут Карина, мне 21 год. Изначально я юрист, усердно училась и мечтала реализоваться в этой сфере, но что-то перещёлкнуло, и любовь к рисованию все сильнее стала тянуть одеяло на себя, и я стала мастером татуировки.\n\n"
                "Здоровье и безопасность процесса - это мой приоритет в работе, и поэтому я использую сугубо одноразовые расходные материалы, провожу обязательную дезинфекцию всех несменяемых инструментов.\n\n"
                "Для меня важно, чтобы татуировка была именно украшением, а не просто наклейкой на теле, поэтому как профессионал я всегда подскажу, как выгоднее всего расположить твою идею на теле.\n\n"
                "Здесь можно посмотреть мои работы: https://vk.com/album-211250660_283398158\n"
                "А здесь найдешь свободные эскизы: https://vk.com/album-211250660_2833977022.")
    bot.send_message(message.chat.id, response, reply_markup=create_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Как подготовиться к сеансу?')
def how_to_prepare(message):
    response = (
        "Сеанс татуировки - это большой стресс для организма, поэтому стоит подготовиться к нему, чтобы чувствовать себя лучше и комфортнее.\n\n"
        "Что нужно для этого сделать?\n"
        "• Хорошо выспаться. Тебе понадобится много сил!\n"
        "• Плотно позавтракать.\n"
        "• Съесть и взять с собой что-нибудь сладкое. Это нужно для того, чтобы твой уровень сахара не упал во время сеанса.\n"
        "• Надеть удобную одежду, которая не сковывает движения. Лучше темных оттенков!\n"
        "• Возьми с собой зарядку, планшет, книгу, наушники. Сеанс будет долгим, так что нужно взять что-то, чем ты будешь отвлекаться.\n\n"
        "Сделай это за два дня до сеанса:\n"
        "• Не пей кофе/энергетики.\n"
        "• За пять дней до сеанса не пей алкоголь.\n"
        "• Помажь место нанесения татуировки увлажняющим кремом.\n"
        "• В день сеанса не пей обезбаливающие препараты.")
    bot.send_message(message.chat.id, response, reply_markup=create_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Как записаться на сеанс?')
def how_to_book(message):
    response = ("Спасибо за проявленный тобой интерес к моей работе!\n\n"
                "Когда я напишу тебе, постарайся четко описать свою идею. Для этого ты можешь прикрепить картинки или фото, которые тебе понравились.\n"
                "Также укажи примерный размер в сантиметрах.\n"
                "После того, как мы определимся с тем, что хотим видеть, и внесения предоплаты, я сообщу тебе свободные для сеанса даты, мы договоримся о времени встречи.")
    bot.send_message(message.chat.id, response, reply_markup=create_keyboard())


# Опрос
@bot.message_handler(func=lambda message: message.text == 'Начать опрос')
def ask_idea(message):
    bot.send_message(message.chat.id, "Опишите вашу идею татуировки:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_style)


# Новый вопрос: стиль татуировки
def ask_style(message):
    client_data['idea'] = message.text
    bot.send_message(message.chat.id,
                     "Какой стиль татуировки вы предпочитаете? (например, реализм, минимализм, традиционный и т.д.)",
                     reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_color)


# Новый вопрос: цвет татуировки
def ask_color(message):
    client_data['style'] = message.text
    bot.send_message(message.chat.id, "Какие цвета будут использоваться? (например, черно-белый, цветной и т.д.)",
                     reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_size)


# Новый вопрос: размер татуировки
def ask_size(message):
    client_data['color'] = message.text
    bot.send_message(message.chat.id, "Какой размер татуировки вас интересует? (например, маленькая, средняя, большая)",
                     reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_budget)


def ask_budget(message):
    client_data['size'] = message.text
    bot.send_message(message.chat.id, "Укажите бюджет:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_contact_info)


def ask_contact_info(message):
    client_data['budget'] = message.text
    bot.send_message(message.chat.id, "Укажите ваш номер телефона:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_telegram_nick)


def ask_telegram_nick(message):
    client_data['phone'] = message.text
    bot.send_message(message.chat.id, "Укажите ваш ник в Telegram:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_preferred_dates)


# Ввод удобных дат
def ask_preferred_dates(message):
    client_data['telegram_nick'] = message.text
    bot.send_message(message.chat.id, "Укажите, какие даты вам подходят для сеанса (например, 10, 15, 20 октября):",
                     reply_markup=create_keyboard())
    bot.register_next_step_handler(message, ask_confirmation)


def ask_confirmation(message):
    client_data['preferred_dates'] = message.text
    confirmation_markup = create_keyboard()
    confirm_button = types.KeyboardButton('Подтвердить запись')
    edit_button = types.KeyboardButton('Редактировать данные')
    confirmation_markup.add(confirm_button, edit_button)

    confirmation_text = ("Вы уверены, что хотите записаться на сеанс с следующими данными?\n\n"
                         f"Идея: {client_data['idea']}\n"
                         f"Стиль: {client_data['style']}\n"
                         f"Цвет: {client_data['color']}\n"
                         f"Размер: {client_data['size']}\n"
                         f"Бюджет: {client_data['budget']}\n"
                         f"Телефон: {client_data['phone']}\n"
                         f"Ник в Telegram: {client_data['telegram_nick']}\n"
                         f"Предпочтительные даты: {client_data['preferred_dates']}\n")
    bot.send_message(message.chat.id, confirmation_text, reply_markup=confirmation_markup)
    bot.register_next_step_handler(message, process_confirmation)


def process_confirmation(message):
    if message.text == 'Подтвердить запись':
        bot.send_message(message.chat.id, "Запись успешно подтверждена! Я свяжусь с вами для дальнейших деталей.",
                         reply_markup=create_keyboard())
        send_to_master(message)  # Пересылка данных мастеру
    elif message.text == 'Редактировать данные':
        edit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        edit_markup.add(types.KeyboardButton('Ред. идею'),
                        types.KeyboardButton('Ред. стиль'),
                        types.KeyboardButton('Ред. цвет'),
                        types.KeyboardButton('Ред. размер'),
                        types.KeyboardButton('Ред. бюджет'),
                        types.KeyboardButton('Ред. телефон'),
                        types.KeyboardButton('Ред. ник в Telegram'),
                        types.KeyboardButton('Ред. предпочтительные даты'),
                        types.KeyboardButton('Завершить редактирование'))
        bot.send_message(message.chat.id, "Выберите, что хотите редактировать:", reply_markup=edit_markup)
        bot.register_next_step_handler(message, edit_data)


def edit_data(message):
    if message.text == 'Ред. идею':
        bot.send_message(message.chat.id, "Опишите вашу идею татуировки:")
        bot.register_next_step_handler(message, update_idea)
    elif message.text == 'Ред. стиль':
        bot.send_message(message.chat.id, "Какой стиль татуировки вы предпочитаете?")
        bot.register_next_step_handler(message, update_style)
    elif message.text == 'Ред. цвет':
        bot.send_message(message.chat.id, "Какие цвета будут использоваться?")
        bot.register_next_step_handler(message, update_color)
    elif message.text == 'Ред. размер':
        bot.send_message(message.chat.id, "Какой размер татуировки вас интересует?")
        bot.register_next_step_handler(message, update_size)
    elif message.text == 'Ред. бюджет':
        bot.send_message(message.chat.id, "Укажите бюджет:")
        bot.register_next_step_handler(message, update_budget)
    elif message.text == 'Ред. телефон':
        bot.send_message(message.chat.id, "Укажите ваш номер телефона:")
        bot.register_next_step_handler(message, update_phone)
    elif message.text == 'Ред. ник в Telegram':
        bot.send_message(message.chat.id, "Укажите ваш ник в Telegram:")
        bot.register_next_step_handler(message, update_telegram_nick)
    elif message.text == 'Ред. предпочтительные даты':
        bot.send_message(message.chat.id, "Укажите, какие даты вам подходят для сеанса:")
        bot.register_next_step_handler(message, update_preferred_dates)
    elif message.text == 'Завершить редактирование':
        bot.send_message(message.chat.id, "Редактирование завершено. Выберите дальнейшие действия:",
                         reply_markup=create_keyboard())
        ask_confirmation(message)  # Добавляем запрос на подтверждение после завершения редактирования


def update_idea(message):
    client_data['idea'] = message.text
    bot.send_message(message.chat.id, "Идея обновлена. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_style(message):
    client_data['style'] = message.text
    bot.send_message(message.chat.id, "Стиль обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_color(message):
    client_data['color'] = message.text
    bot.send_message(message.chat.id, "Цвет обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_size(message):
    client_data['size'] = message.text
    bot.send_message(message.chat.id, "Размер обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_budget(message):
    client_data['budget'] = message.text
    bot.send_message(message.chat.id, "Бюджет обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_phone(message):
    client_data['phone'] = message.text
    bot.send_message(message.chat.id, "Телефон обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_telegram_nick(message):
    client_data['telegram_nick'] = message.text
    bot.send_message(message.chat.id, "Ник в Telegram обновлен. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


def update_preferred_dates(message):
    client_data['preferred_dates'] = message.text
    bot.send_message(message.chat.id, "Предпочтительные даты обновлены. Выберите, что хотите редактировать:",
                     reply_markup=create_keyboard())
    ask_confirmation(message)


# Пересылка данных мастеру
def send_to_master(message):
    master_chat_id = Chat_id  # Замените на chat_id мастера
    message_text = (f"Новая запись:\n"
                    f"Идея: {client_data['idea']}\n"
                    f"Стиль: {client_data['style']}\n"
                    f"Цвет: {client_data['color']}\n"
                    f"Размер: {client_data['size']}\n"
                    f"Бюджет: {client_data['budget']}\n"
                    f"Телефон: {client_data['phone']}\n"
                    f"Ник в Telegram: {client_data['telegram_nick']}\n"
                    f"Предпочтительные даты: {client_data['preferred_dates']}\n")
    bot.send_message(master_chat_id, message_text)


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
