################################################################################################
#     ███████╗ ██████╗ ██████╗ ███████╗███████╗████████╗██╗    ██████╗  ██████╗ ████████╗      #
#     ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██╔══██╗██╔═══██╗╚══██╔══╝      #
#     █████╗  ██║   ██║██████╔╝█████╗  ███████╗   ██║   ██║    ██████╔╝██║   ██║   ██║         #
#     ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ╚════██║   ██║   ██║    ██╔══██╗██║   ██║   ██║         #
#     ██║     ╚██████╔╝██║  ██║███████╗███████║   ██║   ██║    ██████╔╝╚██████╔╝   ██║         #
#     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝         #
################################################################################################
# Библиотека
import telebot, pyowm, bs4, requests, COVID19Py, youtube_dl, os
from telebot import types
from time import gmtime, strftime
from instalooter.looters import PostLooter
from ft_terminal import trm_star, trm_txt, trm_txt_call, trm_launch
from configbot import TOKEN, admin_id, banlist, version
from mat import matlist
from utils import getanekdot, weather_owm, covid, youtube_audio, youtube_video, instagram_v, instagram_p
################################################################################################
###                                         API                                              ###
################################################################################################
#Токен
bot = telebot.TeleBot(TOKEN)
covid19 = COVID19Py.COVID19()
################################################################################################
###                                      DB log                                              ###
################################################################################################
# Сохраняется все записи пользователей в отдельный файл ft_log.txt и rate.txt
def log(time, message):
    log_print(time, message.from_user.first_name, message.from_user.username, message.chat.id, message.text)

def log_print(time, name, user, user_id, command):
    log_file = open('ft_log.txt', 'a')
    log_file.write('{} - Имя: {} / Username: @{} / ID: {} -> \"{}\"\n'.format(time, name, user, user_id, command))
    log_file.close()

def rate(time, call):
    rate_print(time, call.data)

def rate_print(time, rate):
    rate_file = open('rate.txt', 'a')
    rate_file.write('{} / Поставили звезд -> \"{}\"\n'.format(time, rate))
    rate_file.close()
################################################################################################
###                                       Команды                                            ###
################################################################################################
             ###                      Команда /start                      ###
             ################################################################
@bot.message_handler(commands=['start'])    # Принимает команду
def welcome(message):   # Функция
    bot.delete_message(message.chat.id, message.message_id) #Удаляеть пред. сообщение
    if message.from_user.id == banlist:     # Бан юзеров
        delet = types.ReplyKeyboardRemove() # Удаление клавиатуры

        # Отправка сообщении
        file_id = 'CAACAgIAAxkBAAJJa16aMaDA7qpL2prtgpPnZ7vGNVe0AAJ-BQACztjoC9E5b_hSh1A0GAQ'
        bot.send_sticker(message.chat.id, file_id)
        bot.send_message(message.chat.id, 'ВЫ БЫЛИ ЗАБАНЕНЫ!', reply_markup=delet)
    else:
        # Сообщение для администратора сервера в лог ft_log.txt
        answer = "Запустил(а) бота!"
        trm_txt(message, answer)
        log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)

        # Отправка сообщении
        file_id = 'CAACAgIAAxkBAAJJaV6aMWT4JQbsYEVZZ7VivtL_YV6PAAJtBQACztjoC70P1nRDCpMcGAQ'
        bot.send_sticker(message.chat.id, file_id)
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, ваш помощник в социальных сетях.".format(message.from_user, bot.get_me()), parse_mode='html')

        # Активация главной клавиатуры
        mainkeyboard(message)
################################################################
###                      Команда /help                       ###
################################################################
@bot.message_handler(commands=['help'])
def help(message):
    # Отправка сообщении
    file_id = 'CAACAgIAAxkBAAJJbV6aMez2goOqWyyrNg06bZeg8xmXAAKmBQACztjoC8vKTTQSsWS3GAQ'
    bot.send_sticker(message.chat.id, file_id)
    bot.send_message(message.chat.id, "Если у вас возникли проблемы обратитесь к администратору!", parse_mode='markdown')
################################################################
###                Команда /status для админа                ###
################################################################
@bot.message_handler(commands=['status'])
def status(message):
    if message.from_user.id == admin_id:
        username = 'nurmukhammed'
        token = 'df4e728fe8d263cdb6aa32439e15651d6bafeb55'

        response = requests.get(
          'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(username=username
         ),
          headers={'Authorization': 'Token {token}'.format(token=token)}
        )
        mess = ('Получил неожиданный код статуса {}: \n{!r}'.format(response.status_code, response.content))

        # Отправка сообщении
        bot.send_message(message.chat.id, "Статус сервера: \n" + mess)
    else:
        bot.send_message(message.chat.id, "Доступ запрещен!")
################################################################################################
###                                       Короновирус                                        ###
################################################################################################
def cvd_panel(message):
    global cvd_sticker
    # Клавиатура
    markup = types.InlineKeyboardMarkup(row_width=2)

    ru = types.InlineKeyboardButton("Россия🇷🇺", callback_data='ru_cvd')
    kz = types.InlineKeyboardButton("Казахстан🇰🇿", callback_data='kz_cvd')
    bl = types.InlineKeyboardButton("Беларусия🇧🇾", callback_data='bl_cvd')
    uk = types.InlineKeyboardButton("Украина🇺🇦", callback_data='uk_cvd')
    world = types.InlineKeyboardButton("Мир 🌏", callback_data='world_cvd')
    us = types.InlineKeyboardButton("США 🇺🇸", callback_data='us_cvd')
    it = types.InlineKeyboardButton("Италия 🇮🇹", callback_data='it_cvd')
    uz = types.InlineKeyboardButton("Узбекистан 🇺🇿", callback_data='uz_cvd')
    pl = types.InlineKeyboardButton("Польша 🇵🇱", callback_data='pl_cvd')

    markup.add(world)
    markup.add(ru, kz)
    markup.add(bl, uk)
    markup.add(us, it)
    markup.add(uz, pl)

    # Отправка сообщении
    file_id = 'CAACAgIAAxkBAAJHr16XGp5ZZwRzJjyw7ZuejrB4sHE8AALyAQACVp29CgqJR4ysf4fyGAQ'
    cvd_sticker = bot.send_sticker(message.chat.id, file_id)
    bot.send_message(message.chat.id, 'Выберите страну:', reply_markup=markup)
################################################################################################
###                                       Функция                                            ###
################################################################################################
             ###                    Func главный панель                   ###
             ################################################################
def mainkeyboard(message):
    # Клавиатура
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)

    next = types.KeyboardButton("[Далее]")
    social = types.KeyboardButton("Соц.Сети📱")
    games = types.KeyboardButton("Игры 🎮")
    weather = types.KeyboardButton("Погода ⛅️")
    anekdot = types.KeyboardButton("Анекдот😂")
    virus = types.KeyboardButton("COVID-19🦠")

    key.row(social)
    key.row(games, anekdot)
    key.row(weather, virus)
    key.row(next)

    # Отправка сообщении
    bot.send_message(message.chat.id, '`Выберите` `интересующий` `вас` `раздел:`', reply_markup=key, parse_mode='markdown', disable_web_page_preview=True)
################################################################################################
###                                     FUNC СЛЕД СТР                                        ###
################################################################################################
def next(message):
    # Клавиатура
    types.ReplyKeyboardRemove()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    versionbb = types.KeyboardButton("Версия БОТа 🤖")
    creator = types.KeyboardButton("Создатели 👨🏻‍💻")
    callback = types.KeyboardButton("Обратная связь 📞")
    back = types.KeyboardButton("[Назад]")
    review = types.KeyboardButton("Оставить отзыв ⭐️")
    markup.add(versionbb, creator)
    markup.add(review, callback)
    markup.add(back)

    # Отправка сообщении
    bot.send_message(message.chat.id, '`Выберите` `интересующий` `вас` `раздел:`', reply_markup=markup, parse_mode='markdown')
################################################################################################
###                                      FUNC CALLBACK                                         ###
################################################################################################
def callback(message):
    # Отправка сообщении
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALWX17AnORPgLIBY3RIocHzBGWUGWewAAIaAAMjW_IJ8IzfaHg6wlUZBA')
    bot.send_message(message.chat.id, 'Если у вас возникли проблемы, напишите на почту:\
                                        \nnazarex1020@gmail.com или же [сюда](https://t.me/nagiez)', parse_mode='markdown', disable_web_page_preview=True)
################################################################################################
###                                      FUNC CREATOR                                        ###
################################################################################################
def creator(message):
    # Отправка сообщении
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALWY17AnT7amOqOj-rFUOwZLikhLwuwAAIeAAMjW_IJb0c04k_wMecZBA')
    bot.send_message(message.chat.id, 'Данный телеграм бот был создан командой *Foresti* *Team* \
                                                                                                \n\
                                                                                                \n*Разработчик:* `Нурмухаммед` `Бостан` \
                                                                                                \n*Аналитик:* `Михаил` `Сухов`\
                                                                                                \n*Тестировщик*: `Илья` `Конощенок`\
                                                                                                \n*Менеджер* *проекта:* `Илья` `Бугаёв`',
                                                                                                parse_mode='markdown')
################################################################################################
###                                      FUNC SOCIAL                                         ###
################################################################################################
def call_social(message):
    # Клавиатура
    markup = types.InlineKeyboardMarkup(row_width=2)

    video_in_audio_yt = types.InlineKeyboardButton("Конвертация видео в аудио из YouTube", callback_data='v_i_a_yt')
    dwnl_video_yt = types.InlineKeyboardButton("Скачать видео из YouTube", callback_data='d_v_yt')
    dwnl_photo_ins = types.InlineKeyboardButton("Скачать фото из Instagram", callback_data='d_p_ins')
    dwnl_video_ins = types.InlineKeyboardButton("Скачать видео из Instagram", callback_data='d_v_ins')

    markup.add(video_in_audio_yt)
    markup.add(dwnl_video_yt)
    markup.add(dwnl_photo_ins)
    markup.add(dwnl_video_ins)

    # Отправка сообщении
    file_id = 'CAACAgIAAxkBAAJJcV6aMmuDvoXyeIz9XG6SYfEAAQjrBwACjQUAAs7Y6AsiezOh7cvX6BgE'
    bot.send_sticker(message.chat.id, file_id)
    bot.send_message(message.chat.id, 'Список функционала:', reply_markup=markup)
################################################################################################
###                                       YouTube                                            ###
################################################################################################
#исключительно принимает текст youtube.com или youtu.be
@bot.message_handler(regexp='youtube.com/\D|youtu.be/')
def general_youtube_function(message):
    # Сохраняем данные что пишет пользователь
    log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
    try:
        # Терминал
        answer = "КОНВЕРТАЦИЯ..."
        trm_txt(message, answer)

        # Переменные для callback yt_audio и yt_video
        global d_file
        global message_send
        global file_caption
        global info

        # Отправка сообщении
        message_send = bot.send_message(message.chat.id, "Обраватываю запрос ...")

        if 'youtube.com' in message.text or 'youtu.be' in message.text:
            with youtube_dl.YoutubeDL() as ydl:
                # Переменные
                d_file = message.text

                # Удаляет сообщение и отправляет новое
                bot.delete_message(message.chat.id, message.message_id)
                message_send = bot.edit_message_text(text="Парсим запрос ...", chat_id=message.chat.id, message_id=message_send.message_id)

                # Парсинг
                info = ydl.extract_info(message.text, download=False)
                file_caption = f"<b>Названия файла:</b> {info['title']} \n<b>Число просмотров:</b> {info['view_count']} \n<b>Число лайков:</b> {info['like_count']} \n<b>Число дизлайков:</b> {info['dislike_count']}"

                # Клавиатура
                start_keyboard = types.InlineKeyboardMarkup()

                b_audio = types.InlineKeyboardButton(text='Скачать аудио', callback_data='yt_audio')
                b_video = types.InlineKeyboardButton(text='Скачать видео', callback_data='yt_video')

                start_keyboard.add(b_audio, b_video)

                # Удаление сообщении
                bot.delete_message(message.chat.id, message_send.message_id)

                # Отправлется обложку фотографии вместе с клавиатурой
                message_send = bot.send_photo(message.chat.id, info["thumbnail"], file_caption, parse_mode="HTML", reply_markup=start_keyboard)

    except:
        # Удаляет сообщение и отправляет новое
        bot.delete_message(message.chat.id, message_send.message_id)
        bot.send_message(message.chat.id, 'Ссылка не действительно!')
################################################################################################
###                                      Instagram                                           ###
################################################################################################
#исключительно принимает текст instagram.com/p/
# @bot.message_handler(regexp='instagram.com/p/')
# def general_instagram_function(message):
#     try:
#         # # Сохраняем данные что пишет пользователь
#         log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
#         try:
#             answer = "СКАЧИВАНИЕ..."
#             trm_txt(message, answer)

#             # Удаляет сообщение и отправляет новое
#             bot.delete_message(message.chat.id, message.message_id)
#             message_send = bot.send_message(message.chat.id, "Парсим запрос ...")

#             # Переменные
#             url = message.text
#             looter = PostLooter(url)
#             # Фото
#             if looter.info['__typename'] == 'GraphImage':
#                 f = instagram_p(url)
#                 # Удаляет сообщение и отправляет новое
#                 bot.delete_message(message.chat.id, message_send.message_id)
#                 bot.send_photo(message.chat.id, f)

#             # Видео
#             elif looter.info['__typename'] == 'GraphVideo':
#                 f = instagram_v(url)
#                 # Удаляет сообщение и отправляет новое
#                 bot.delete_message(message.chat.id, message_send.message_id)
#                 bot.send_video(message.chat.id, f)

#             # Если много фотографии
#             elif looter.info['__typename'] == 'GraphSidecar':
#                 # Удаляет сообщение и отправляет новое
#                 bot.delete_message(message.chat.id, message_send.message_id)
#                 bot.send_message(message.chat.id, 'Извините, я не могу отправить вам сообщение с более чем 1 фотографией!')

#         except:
#             # Удаляет сообщение и отправляет новое
#             bot.delete_message(message.chat.id, message.message_id)
#             bot.send_message(message.chat.id, 'Ссылка не действительно!')

#     except:
#         # Удаляет сообщение и отправляет новое
#         bot.delete_message(message.chat.id, message_send.message_id)
#         bot.send_message(message.chat.id, 'Ошибка!')

@bot.message_handler(regexp='instagram.com/p/')
def general_instagram_function(message):
    # Сохраняем данные что пишет пользователь
    log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
    try:
        # Терминал
        answer = "Скачивание..."
        trm_txt(message, answer)

        global d_file
        global message_send

        # Отправка сообщении
        message_send = bot.send_message(message.chat.id, "Обраватываю запрос ...")

        # Переменные
        d_file = message.text

        # Удаляет сообщение и отправляет новое
        bot.delete_message(message.chat.id, message.message_id)
        message_send = bot.edit_message_text(text="Парсим запрос ...", chat_id=message.chat.id, message_id=message_send.message_id)

        # Клавиатура
        start_keyboard = types.InlineKeyboardMarkup()

        ins_photo = types.InlineKeyboardButton(text='Скачать фото', callback_data='ins_photo')
        ins_video = types.InlineKeyboardButton(text='Скачать видео', callback_data='ins_video')

        start_keyboard.add(ins_photo, ins_video)

        # Удаление сообщении
        bot.delete_message(message.chat.id, message_send.message_id)

        # Отправлется обложку фотографии вместе с клавиатурой
        message_send = bot.send_message(message.chat.id, 'Выберите формат медиафайла:', reply_markup=start_keyboard)

    except:
        # Удаляет сообщение и отправляет новое
        bot.delete_message(message.chat.id, message_send.message_id)
        bot.send_message(message.chat.id, 'Ссылка не действительно!')
################################################################################################
###                                     ввод данных                                          ###
################################################################################################
@bot.message_handler(content_types=['text'])
def text_handler(message):
    # Сохраняем данные что пишет пользователь
    log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
    if message.chat.type == 'private':
        # Пользователь который находиться в бан листе
        if message.from_user.id == banlist:
            # Удаление клавитауры и сообщении
            bot.delete_message(message.chat.id, message.message_id)
            delet = types.ReplyKeyboardRemove()

            # Отправка сообщении
            file_id = 'CAACAgIAAxkBAAI2qF54r4eaZHe6ZZyCBzJg2POqbRWhAAItAQACWQMDAAEt9hslJkzrsRgE'
            bot.send_sticker(message.chat.id, file_id)
            bot.send_message(message.chat.id, 'ВЫ БЫЛИ ЗАБАНЕНЫ!', reply_markup=delet)

        # Пользователь
        else:
            ################################################################################################
            ###                                          Панель                                          ###
            ################################################################################################
            if message.text == 'Погода ⛅️':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Клавитаура
                markup = types.InlineKeyboardMarkup(row_width=2)

                spb = types.InlineKeyboardButton("Санкт-Петербург, РФ 🇷🇺", callback_data='spb1')
                msc = types.InlineKeyboardButton("Москва, РФ 🇷🇺", callback_data='msc1')
                kzn = types.InlineKeyboardButton("Казань, РФ 🇷🇺", callback_data='kzn1')
                ekb = types.InlineKeyboardButton("Екатеринбург, РФ 🇷🇺", callback_data='ekb1')
                nov = types.InlineKeyboardButton("Новосибирск, РФ 🇷🇺", callback_data='nov1')
                kln = types.InlineKeyboardButton("Калининград, РФ 🇷🇺", callback_data='kln1')
                shym = types.InlineKeyboardButton("Шымкент, РК 🇰🇿", callback_data='shym1')
                alm = types.InlineKeyboardButton("Алматы, РК 🇰🇿", callback_data='alm1')
                ast = types.InlineKeyboardButton("Нур-Султан, РК 🇰🇿", callback_data='ast1')
                local = types.InlineKeyboardButton("Отправить ГЕО 📍", callback_data='local')

                markup.add(ast)
                markup.add(alm)
                markup.add(shym)
                markup.add(msc)
                markup.add(spb)
                markup.add(kzn)
                markup.add(ekb)
                markup.add(nov)
                markup.add(kln)
                markup.add(local)

                # Отправка сообщении
                bot.send_message(message.chat.id, 'Список городов:', reply_markup=markup)

            elif message.text == 'COVID-19🦠':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Активация функции
                cvd_panel(message)

            elif message.text == 'Соц.Сети📱':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Удалание сообщении
                bot.delete_message(message.chat.id, message.message_id)

                # Активация функции
                call_social(message)

            elif message.text == 'Оставить отзыв ⭐️':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)

                item1 = types.InlineKeyboardButton("⭐️", callback_data='star_1')
                item2 = types.InlineKeyboardButton("⭐️⭐️", callback_data='star_2')
                item3 = types.InlineKeyboardButton("⭐️⭐️⭐️", callback_data='star_3')
                item4 = types.InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data='star_4')
                item5 = types.InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data='star_5')

                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                markup.add(item5)
                # Отправка сообщении
                bot.send_message(message.chat.id, 'Оцените наш телеграм бот', reply_markup=markup)

            elif message.text == '[Далее]':
                # Терминал
                answer = "Переход СТР 2"
                trm_txt(message, answer)

                # Активация функции
                next(message)

            elif message.text == '[Назад]':
                # Терминал
                answer = "Переход СТР 1"
                trm_txt(message, answer)

                # Активация функции
                mainkeyboard(message)

            elif message.text == 'Версия БОТа 🤖':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Активация функции
                bot.send_message(message.chat.id, 'Версия бота: ' + version, parse_mode='markdown')

            elif message.text == 'Создатели 👨🏻‍💻':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Активация функции
                creator(message)

            elif message.text == 'Обратная связь 📞':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Активация функции
                callback(message)

            elif message.text == 'Игры 🎮':
                # Терминал
                answer = "Вызвал функцию"
                trm_txt(message, answer)

                # Инлайн клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)

                gms = types.InlineKeyboardButton(text='перейти', url='https://t.me/gamee', callback_data='gms')

                markup.add(gms)

                # Удаляет сообщение и отправляет новое
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJXNF6kyU-GQtUVZ053SEAMFB9RLmHSAAIZAANOXNIpT7YS3XX2CugZBA')
                bot.send_message(message.chat.id, 'Вот ссылка на бота, где можно поиграть прямо в телеграме', reply_markup=markup)

            elif message.text == 'Анекдот😂':
                # Терминал
                answer = "Хочет почитать анекдота"
                trm_txt(message, answer)

                # Отправка сообщении
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, getanekdot())
            ################################################################################################
            #                                         Пасхальное яйцо                                      #
            ################################################################################################
            elif message.text == 'frog' or message.text == 'Frog':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAIx0l5qeu-IDGRasmaNpRkWBVqDDabQAAIFAAN1UIETZmBnin0s48QYBA'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Молодец, ты нашел(нашла) пасхалку!')

            elif message.text == 'Cat' or message.text == 'cat':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJdm16v_tLenG8hk_GKQ3Ip8sAeHARzAAJNOgAC6VUFGGwZRSkZy7lYGQQ'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Молодец, ты нашел(нашла) пасхалку!')

            elif message.text == 'Dog' or message.text == 'dog':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJiV6aNbsOQZ0NlZTXaRYZ0j_nYZqxAAIHAAOKfy43zv_oD7S3blYYBA'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Молодец, ты нашел(нашла) пасхалку!')

            elif message.text == 'Freeman' or message.text == 'freeman':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgQAAxkBAAIx1F5qe7vr5tUe-ROJwKTyaRwkSvemAAJRAAODatAQ9LqbS-wgwS8YBA'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Я вам ничего не должен, это вы должны себе.')

            elif message.text == 'no rules' or message.text == 'No rules' or message.text == '/no_rules' or message.text == 'no rules!' or message.text == 'No rules!' or message.text == 'party hard' or message.text == 'Party hard':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                bot.send_chat_action(message.chat.id, 'find_location')
                file_id = 'CAACAgIAAxkBAAJJdV6aMsIIj21ygdN9Ssm9sTQJptcRAAKLBQACztjoC6GpRX_jrcCsGAQ'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Го тусить!')

            elif message.text == 'танцуем' or message.text == 'Танцуем' or message.text == 'dance' or message.text == 'Dance':
                # Терминал
                answer = "Нашел(нашла) пасхалку!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJYOV6nqnigM3oM4OxlMtOyEtvCbi34AAKIBQACztjoC231wM7ctbTjGQQ'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Танцуй!')
            ################################################################################################
            ###                                      Фильтр мата                                         ###
            ################################################################################################
            elif message.text in matlist:
                # Удаление сообщении
                bot.delete_message(message.chat.id, message.message_id)

                # Терминал
                answer = "Обзывается!"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJXKl6kxsJrbadcC-M3ym4Y2KEoKpojAAKABQACztjoC_0ko1cTLd39GQQ'
                bot.send_sticker(message.chat.id, file_id)
            ################################################################################################
            ###                             Значение ELSE в текстовых сообщениях                         ###
            ################################################################################################
            else:
                # Терминал
                answer = "ПИШЕТ ДИЧЬ"
                trm_txt(message, answer)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJd16aMxnK0_4SE4Swc17FUSL5e6wLAAKlBQACztjoC-kLCo3s8H9xGAQ'
                bot.send_sticker(message.chat.id, file_id)
                bot.send_message(message.chat.id, 'Я не знаю что ответить!')
################################################################################################
###                                     Call back inline keyboards                           ###
################################################################################################
#InlineKeyboards ответочка
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            ################################################################################################
            ###                                CALLBACK Оставить отзыв                                   ###
            ################################################################################################
            if call.data == 'star_1':
                rate(strftime("%Y-%m-%d %H:%M:%S", gmtime()), call)

                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                callans = "1"
                trm_star(call, callans)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJeV6aMy1hWwz0Xh2mqJSqCVyZF9TxAAJ6BQACztjoC2HJ4Rcvib92GAQ'
                sti = bot.send_sticker(call.message.chat.id, file_id)
                bot.send_message(call.message.chat.id, 'Возможно, это не для Вас.')

            elif call.data == 'star_2':
                rate(strftime("%Y-%m-%d %H:%M:%S", gmtime()), call)

                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                callans = "2"
                trm_star(call, callans)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJe16aMznGD4e4CL0w4zBOY_XI4i2sAAJ8BQACztjoC_7XeYL8ab6XGAQ'
                sti = bot.send_sticker(call.message.chat.id, file_id)
                bot.send_message(call.message.chat.id, 'Мы работаем над ошибками.')

            elif call.data == 'star_3':
                rate(strftime("%Y-%m-%d %H:%M:%S", gmtime()), call)

                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                callans = "3"
                trm_star(call, callans)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJfV6aM06fBSwiFrxMwR9i3h5NZUT1AAKMBQACztjoC4V1-fyGKIxNGAQ'
                sti = bot.send_sticker(call.message.chat.id, file_id)
                bot.send_message(call.message.chat.id, 'Будем стараться!')

            elif call.data == 'star_4':
                rate(strftime("%Y-%m-%d %H:%M:%S", gmtime()), call)

                # Отправка сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                callans = "4"
                trm_star(call, callans)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJf16aM1u0lPf2abnujaJQrmy4AoOLAAKiBQACztjoC61sVQ-LShGEGAQ'
                sti = bot.send_sticker(call.message.chat.id, file_id)
                bot.send_message(call.message.chat.id, 'Спасибо. Заходите еще!')

            elif call.data == 'star_5':
                rate(strftime("%Y-%m-%d %H:%M:%S", gmtime()), call)

                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                callans = "5"
                trm_star(call, callans)

                # Отправка сообщении
                file_id = 'CAACAgIAAxkBAAJJgV6aM2dC8hez2d9BmE7U3cHD_q2QAAKBBQACztjoC8fgM5-5KThxGAQ'
                sti = bot.send_sticker(call.message.chat.id, file_id)
                bot.send_message(call.message.chat.id, 'И мы тебя любим!', sti)
            ################################################################################################
            ###                                  CALLBACK Погода                                         ###
            ################################################################################################
            elif call.data == 'msc1':
                try:
                    # Переменные
                    weather_city = "Moscow,RU"
                    weather_city1 = "Москва"
                    weather_city2 = "Москве"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'spb1':
                try:
                    # Переменные
                    weather_city = "Saint Petersburg, RU"
                    weather_city1 = "Санкт-Петербург"
                    weather_city2 = "Питере"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'kzn1':
                try:
                    # Переменные
                    weather_city = "Kazan', RU"
                    weather_city1 = "Казань"
                    weather_city2 = "Казани"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'ekb1':
                try:
                    # Переменные
                    weather_city = "Ekaterinburg, RU"
                    weather_city1 = "Екатеринбург"
                    weather_city2 = "Екатеринбурге"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'nov1':
                try:
                # Переменные
                    weather_city = "Novosibirsk, RU"
                    weather_city1 = "Новосибирск"
                    weather_city2 = "Новосибирске"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'kln1':
                try:
                    # Переменные
                    weather_city = "Kaliningrad, RU"
                    weather_city1 = "Калининград"
                    weather_city2 = "Калининграде"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'shym1':
                try:
                    # Переменные
                    weather_city = "Shymkent, KZ"
                    weather_city1 = "Шымкент"
                    weather_city2 = "Шымкенте"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'alm1':
                try:
                    # Переменные
                    weather_city = "Almaty, KZ"
                    weather_city1 = "Алматы"
                    weather_city2 = "Алмате"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'ast1':
                try:
                    # Переменные
                    weather_city = "Nur-Sultan,KZ"
                    weather_city1 = "Нур-Султан"
                    weather_city2 = "Нур-Султане"

                    # Активация функции
                    mess = weather_owm(weather_city, weather_city1, weather_city2)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess)
                except:
                    # Отправка сообщении
                    bot.send_message(call.message.chat.id, "Произошла ошибка!")

            elif call.data == 'local':
                global weather_local

                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Клавиатура
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

                button_geo = types.KeyboardButton(text="Отправить местоположение 📍", request_location=True)

                back = types.KeyboardButton(text="[Назад]")

                keyboard.add(button_geo)
                keyboard.add(back)

                # Отправка сообщении
                weather_local = bot.send_message(call.message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение, для получения сведений о погоде.", reply_markup=keyboard)
            ################################################################################################
            ###                                     CALLBACK Соц. сети                                   ###
            ################################################################################################
            elif call.data == 'callback_func':
                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)

                video_in_audio_yt = types.InlineKeyboardButton("Конвертация видео в аудио из YouTube", callback_data='v_i_a_yt')
                dwnl_video_yt = types.InlineKeyboardButton("Скачать видео из YouTube", callback_data='d_v_yt')
                dwnl_photo_ins = types.InlineKeyboardButton("Скачать фото из Instagram", callback_data='d_p_ins')
                dwnl_video_ins = types.InlineKeyboardButton("Скачать видео из Instagram", callback_data='d_v_ins')

                markup.add(video_in_audio_yt)
                markup.add(dwnl_video_yt)
                markup.add(dwnl_photo_ins)
                markup.add(dwnl_video_ins)

                # Удаляет сообщение и отправляет новое
                bot.send_message(call.message.chat.id, 'Список функционала:', reply_markup=markup)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif call.data == 'v_i_a_yt':
                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                ansfunc = ("Хочеть конвертировать видео в аудио из YouTube")
                trm_txt_call(call, ansfunc)

                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)
                back_func = types.InlineKeyboardButton(text='назад', callback_data= 'callback_func' )
                markup.add(back_func)

                # Отправка сообщении
                bot.send_message(call.message.chat.id, '\n*Инструкция*:\
                                                        \n1. Отправьте мне ссылку на видео из YouTube"\
                                                        \n2. Нажмите на кнопку "Скачать аудио"\
                                                        \n3. Ждите несколько секунд[.](https://i.imgur.com/n762bJ0.mp4)', parse_mode='markdown', reply_markup=markup)
            elif call.data == 'd_v_yt':
                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                ansfunc = ("Хочеть скачать видео из YouTube")
                trm_txt_call(call, ansfunc)

                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)
                back_func = types.InlineKeyboardButton(text='назад', callback_data= 'callback_func' )
                markup.add(back_func)

                # Отправка сообщении
                bot.send_message(call.message.chat.id, '\n*Инструкция*:\
                                                        \n1. Отправьте мне ссылку на видео из YouTube"\
                                                        \n2. Нажмите на кнопку "Скачать видео"\
                                                        \n3. Ждите несколько секунд[.](https://i.imgur.com/tPBToFx.mp4)\
                                                        \n\nЕсли у вас видео не открывается, сохраните ее в галерею.', parse_mode='markdown', reply_markup=markup)

            elif call.data == 'd_p_ins':
                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Терминал
                ansfunc = ("Хочеть скачать фото из Instagram")
                trm_txt_call(call, ansfunc)

                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)
                back_func = types.InlineKeyboardButton(text='назад', callback_data= 'callback_func' )
                markup.add(back_func)

                # Отправка сообщении
                bot.send_message(call.message.chat.id, '\n*Инструкция*:\
                                                        \n1. Отправьте мне ссылку на пост из Instagram"\
                                                        \n2. Ждите несколько секунд[.](https://i.imgur.com/e84iMcS.mp4)', parse_mode='markdown', reply_markup=markup)

            elif call.data == 'd_v_ins':
                # Удаление сообщении
                bot.delete_message(call.message.chat.id, call.message.message_id)

                ansfunc = ("Хочеть скачать видео из Instagram")
                trm_txt_call(call, ansfunc)

                # Клавиатура
                markup = types.InlineKeyboardMarkup(row_width=2)
                back_func = types.InlineKeyboardButton(text='назад', callback_data= 'callback_func' )
                markup.add(back_func)

                # Отправка сообщении
                bot.send_message(call.message.chat.id, '\n*Инструкция*:\
                                                        \n1. Отправьте мне ссылку на пост из Instagram"\
                                                        \n2. Ждите несколько секунд[.](https://i.imgur.com/PzY2ZjK.mp4)', parse_mode='markdown', reply_markup=markup)
            ################################################################################################
            ###                                      CALL BACK COVID-19 Страны                           ###
            ################################################################################################
            elif call.data == 'ru_cvd':
                try:
                    # Код страны
                    country = "RU"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'kz_cvd':
                try:
                    # Код страны
                    country = "KZ"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'bl_cvd':
                try:
                    # Код страны
                    country = "BY"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'uk_cvd':
                try:
                    # Код страны
                    country = "UA"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'uz_cvd':
                try:
                    # Код страны
                    country = "UZ"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'it_cvd':
                try:
                    # Код страны
                    country = "IT"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'us_cvd':
                try:
                    # Код страны
                    country = "US"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'pl_cvd':
                try:
                    # Код страны
                    country = "PL"
                    mess = covid(country)
                    site = "\n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"
                    # Удаление и отправляет сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, mess + site, parse_mode='markdown', disable_web_page_preview=True)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")

            elif call.data == 'world_cvd':
                try:

                    location = covid19.getLatest()

                    # Удаление и отправляет сообщении
                    mess = f"""В *Мире 🌏* \nЗаражений за всё время: {location['confirmed']} \nСмертей: *{location['deaths']}* \n[Подробнее...](https://yandex.ru/maps/covid19) \n\n[Рекомендации от ВОЗ](https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019/advice-for-public)"""
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJG8F6V1CPNwH5Aywe4AAG-xgEosWAWuAAC5wEAAladvQoNeVnL-khcCxgE')
                    bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                    bot.send_message(call.message.chat.id, mess, parse_mode='markdown', disable_web_page_preview=True)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except:
                    try:
                        bot.delete_message(call.message.chat.id, cvd_sticker.message_id)
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                    except:
                        pass
                    bot.send_message(call.message.chat.id, "Ошибка!")
            ################################################################################################
            ###                                      CALL BACK YouTube Скачаивание                       ###
            ################################################################################################
            # АУДИО
            elif call.data == 'yt_audio':
                try:
                    # Удаление и отправляет сообщении
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    sticker = bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYfl6oN83NmqxMlb34jgLPSzwLAAFJ7QACUQsAAi8P8AbEnRxfDMOXhhkE')
                    message_send = bot.send_message(call.message.chat.id, "Загрузка...")

                    # Импорт файла
                    audio = youtube_audio(d_file, info)

                    # Отправка файла
                    bot.send_audio(call.message.chat.id, audio, "`Название:`\n" + info['title'], parse_mode="markdown", timeout=200)

                    # Удаление файла из директории
                    os.remove(info['id'] + '.mp3')

                    #Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 1')
                except:
                    # Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 2')

                    # Отправка сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYgl6oN_mdmpJbJSUf_tnyzoXFRuM6AAIlCwACLw_wBjxmHG5qqhRaGQQ')
                    bot.send_message(call.message.chat.id, 'Ошибка! Повторите попытку позже!')
            ################################################################################################
            # ВИДЕО
            elif call.data == 'yt_video':
                try:
                    # Удаление и отправляет сообщении
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    sticker = bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYfl6oN83NmqxMlb34jgLPSzwLAAFJ7QACUQsAAi8P8AbEnRxfDMOXhhkE')
                    message_send = bot.send_message(call.message.chat.id, "Загрузка...")

                    # Импорт файла
                    video = youtube_video(d_file, info)

                    # Отправка файла
                    bot.send_video(call.message.chat.id, video)
                    bot.send_message(call.message.chat.id, "`Название:`\n" + info['title'], parse_mode="markdown")

                    # Удаление файла из директории
                    os.remove(info['id'] + '.mp4')

                    # Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 1')
                except:
                    # Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 2')

                    # Отправка сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYgl6oN_mdmpJbJSUf_tnyzoXFRuM6AAIlCwACLw_wBjxmHG5qqhRaGQQ')
                    bot.send_message(call.message.chat.id, 'Ошибка! Повторите попытку позже!')
            ################################################################################################
            ###                                    CALL BACK Instagram Скачаивание                       ###
            ################################################################################################
            #Фото
            elif call.data == 'ins_photo':
                try:
                    # Удаление и отправляет сообщении
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    sticker = bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYfl6oN83NmqxMlb34jgLPSzwLAAFJ7QACUQsAAi8P8AbEnRxfDMOXhhkE')
                    message_send = bot.send_message(call.message.chat.id, "Загрузка...")

                    # Отправка файла
                    bot.send_photo(call.message.chat.id, d_file)
                    #Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 1')
                except:
                    # Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 2')

                    # Отправка сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYgl6oN_mdmpJbJSUf_tnyzoXFRuM6AAIlCwACLw_wBjxmHG5qqhRaGQQ')
                    bot.send_message(call.message.chat.id, 'Ошибка! Повторите попытку позже!')
            ################################################################################################
            #Видео
            elif call.data == 'ins_video':
                try:
                    # Удаление и отправляет сообщении
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    sticker = bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYfl6oN83NmqxMlb34jgLPSzwLAAFJ7QACUQsAAi8P8AbEnRxfDMOXhhkE')
                    message_send = bot.send_message(call.message.chat.id, "Загрузка...")

                    # Отправка файла
                    bot.send_video(call.message.chat.id, d_file)
                    #Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 1')
                except:
                    # Удаление сообщении
                    try:
                        bot.delete_message(call.message.chat.id, sticker.message_id)
                        bot.delete_message(call.message.chat.id, message_send.message_id)
                    except:
                        print('Ошибка удалении! - 2')

                    # Отправка сообщении
                    bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAJYgl6oN_mdmpJbJSUf_tnyzoXFRuM6AAIlCwACLw_wBjxmHG5qqhRaGQQ')
                    bot.send_message(call.message.chat.id, 'Ошибка! Повторите попытку позже!')
            ################################################################################################
    except:
        # Отправка сообщении
        bot.send_message(call.message.chat.id, 'Ошибка! Свяжитесь с Администратором!')
################################################################################################
###                     Принимает локацию от пользователя/погода                             ###
################################################################################################
@bot.message_handler(content_types=["location"])
def location(message):
    try:
        # ID pyowm и язык
        owm = pyowm.OWM('945a394890eab9e4e54bdda87d5e37e7', language="ru")

        # Удаление сообщении
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, weather_local.message_id)

        # Пойск по локации (долгота и широта)
        obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
        w = obs.get_weather()  # поулчаем всю погоду из этого города

        # Достаем инфу
        temp = w.get_temperature('celsius') ["temp"]
        speed = w.get_wind() ["speed"]
        tempmin = w.get_temperature('celsius') ["temp_min"]
        tempmax = w.get_temperature('celsius') ["temp_max"]

        # Разные переменные при каких-то градусов
        if temp < -20:
            answer_weather = "\n\n[Лучше сидеть дома!]"
        elif temp < -10:
            answer_weather = "\n\n[На улице мороз, возми перчатки!]"
        elif temp < 0:
            answer_weather = "\n\n[На улице очень холодно! Не забудь шапку!]"
        elif temp < 15:
            answer_weather = "\n\n[Сейчас холодно, одевайся потеплее.]"
        elif temp < 35:
            answer_weather = "\n\n[Температура норм, надевай что угодно.]"
        else:
            answer_weather = "\n\n[На улице жара]"

        # Клавиатура
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)

        next = types.KeyboardButton("[Далее]")
        social = types.KeyboardButton("Соц.Сети📱")
        games = types.KeyboardButton("Игры 🎮")
        weather = types.KeyboardButton("Погода ⛅️")
        anekdot = types.KeyboardButton("Анекдот😂")
        virus = types.KeyboardButton("COVID-19🦠")

        key.row(social)
        key.row(games, anekdot)
        key.row(weather, virus)
        key.row(next)

        # Отправка сообщении
        bot.send_message(message.chat.id,"В твоем городе, сейчас: " + w.get_detailed_status() + "\nТекущая температура составляет: " + str(temp)+ " °C." + "\nMin/Max = " + str(tempmin) + " / " + str(tempmax) + " °C" + " \nСкорость ветра составляет: " + str(speed) + " м/с" + str(answer_weather), reply_markup=key)

    except:
        # Отправка сообщении
        bot.send_message(message.chat.id, "Произошла ошибка!")
################################################################################################
###                                       Антифлуд                                           ###
################################################################################################
@bot.message_handler(content_types=['sticker', 'audio', 'vidio', 'vidio_note', 'voice', 'photo', 'document', 'emoji'])
def spam_handler(message):
    # Удаляет сообщение
    bot.delete_message(message.chat.id, message.message_id)
################################################################################################
# Сообщение админу
bot.send_message(admin_id, '`СЕРВЕР:` _Бот_ _успешно_ _запущен!_', parse_mode='markdown')
################################################################################################
# Терминал
trm_launch()
################################################################################################
# Запуск бота
bot.polling(none_stop=True, timeout=20)
################################################################################################
#     ███████╗ ██████╗ ██████╗ ███████╗███████╗████████╗██╗    ██████╗  ██████╗ ████████╗      #
#     ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██╔══██╗██╔═══██╗╚══██╔══╝      #
#     █████╗  ██║   ██║██████╔╝█████╗  ███████╗   ██║   ██║    ██████╔╝██║   ██║   ██║         #
#     ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ╚════██║   ██║   ██║    ██╔══██╗██║   ██║   ██║         #
#     ██║     ╚██████╔╝██║  ██║███████╗███████║   ██║   ██║    ██████╔╝╚██████╔╝   ██║         #
#     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝         #
################################################################################################
