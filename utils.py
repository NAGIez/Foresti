import pyowm, bs4, requests, COVID19Py, youtube_dl, os
from instalooter.looters import PostLooter

"""
███████╗████████╗    ██╗   ██╗████████╗██╗██╗     ███████╗
██╔════╝╚══██╔══╝    ██║   ██║╚══██╔══╝██║██║     ██╔════╝
█████╗     ██║       ██║   ██║   ██║   ██║██║     ███████╗
██╔══╝     ██║       ██║   ██║   ██║   ██║██║     ╚════██║
██║        ██║       ╚██████╔╝   ██║   ██║███████╗███████║
╚═╝        ╚═╝        ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝
"""

def getanekdot():
    # Парсинг
    z=''
    s=requests.get('http://anekdotme.ru/random')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('.anekdot_text')
    for x in p:
        s=(x.getText().strip())
        z=z+s+'\n\n'
    return s


def weather_owm(weather_city, weather_city1, weather_city2):
    owm = pyowm.OWM('27d057065c7fb12eb132fe31b42c2195', language = "ru")    # ID pyowm и язык

    observation = owm.weather_at_place(weather_city)    # Выбор локации
    w = observation.get_weather()
    # Достаем инфу
    temp = w.get_temperature('celsius') ["temp"]
    speed = w.get_wind() ["speed"]
    tempmin = w.get_temperature('celsius') ["temp_min"]
    tempmax = w.get_temperature('celsius') ["temp_max"]
    status = w.get_detailed_status()

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

    weather_mess = ("В городе " + weather_city1 + " сейчас: " + status + "\nТекущая температура в " + weather_city2 + " составляет: " + str(temp)+ " °C." + "\nMin/Max = " + str(tempmin) + " / " + str(tempmax) + " °C" + " \nСкорость ветра составляет: " + str(speed) + " м/с" + str(answer_weather))
    return weather_mess

def covid(country):
    covid19 = COVID19Py.COVID19()
    location = covid19.getLocationByCountryCode(country)
    covid_mess = f""" \nНаселение: [{location[0]['country_population']}] \nЗаражений за всё время: [{location[0]['latest']['confirmed']}] \nСмертей: [{location[0]['latest']['deaths']}]"""
    return covid_mess

def youtube_audio(d_file, info):
    # Настройка youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Скачивание и сохранение в директорию
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([d_file])                  # Скачивание
        audio_id = info['id'] + '.mp3'          # ID видео

        files_list = os.listdir(os.getcwd())    # Сохранение в текущую директорию
        for file in files_list:
            if audio_id in file:
                os.renames(file, audio_id)      # Переименование файла
                break

        f_audio = open('./{}'.format(audio_id), 'rb')

        return f_audio

def youtube_video(d_file, info):
    # Настройка youtube_dl
    ydl_opts = {
          'format': 'bestvideo[ext=mp4]+bestaudio[acodec=aac],mp4',
          'audioformat' :'aac',
          'merge_output_format' : 'mp4'
    }

    # Скачивание и сохранение в директорию
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([d_file])                  # Скачивание
        video_id = info['id'] + '.mp4'          # ID видео

        files_list = os.listdir(os.getcwd())    # Сохранение в текущую директорию
        for file in files_list:
            if video_id in file:
                os.renames(file, video_id)      # Переименование файла
                break

        f_video = open('./{}'.format(video_id), 'rb')

        return f_video

def instagram_p(url):
    looter = PostLooter(url)

    # Скачивание
    picture_id = looter.info['id']
    looter.download('./pictures/')

    file = open('./pictures/{}.jpg'.format(picture_id), 'rb')
    return file

def instagram_v(url):
    looter = PostLooter(url)

    # Скачивание
    video_id = looter.info['id']
    looter.download_videos('./videos/')

    file = open('./videos/{}.mp4'.format(video_id), 'rb')
    return file
