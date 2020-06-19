import pytest
import utils
import requests
import os

print("""
███████╗████████╗    ████████╗███████╗███████╗████████╗
██╔════╝╚══██╔══╝    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
█████╗     ██║          ██║   █████╗  ███████╗   ██║   
██╔══╝     ██║          ██║   ██╔══╝  ╚════██║   ██║   
██║        ██║          ██║   ███████╗███████║   ██║   
╚═╝        ╚═╝          ╚═╝   ╚══════╝╚══════╝   ╚═╝   
""")

def test_getanekdot(monkeypatch):
    fakereq = requests.get('http://anekdotme.ru/anekdot/get_7801')
    monkeypatch.setattr(utils.requests, 'get', lambda x: fakereq)
    expected = ('Больше всего мужчин настораживают две вещи: непонятный шум в двигателе автомобиля и девушка, которая вдруг стала такой ласковой и доброй.')
    assert utils.getanekdot().strip() == expected

def test_youtube_download_audio():
    exp_audio = open('./test_file/youtube/audio/short_audio.mp3', 'rb').read()
    f_audio = utils.youtube_audio(
        'https://www.youtube.com/watch?v=fKN6P6xzbPc',
        {'id': 'Самое короткое видео на YouTube-fKN6P6xzbPc'}).read()
    assert f_audio == exp_audio
    os.remove('./Самое короткое видео на YouTube-fKN6P6xzbPc.mp3')

def test_youtube_download_video():
    exp_video = open('./test_file/youtube/video/short_video.mp4', 'rb').read()
    f_video = utils.youtube_video(
        'https://www.youtube.com/watch?v=fKN6P6xzbPc',
        {'id': 'Самое короткое видео на YouTube-fKN6P6xzbPc'}).read()
    assert f_video == exp_video
    os.remove('./Самое короткое видео на YouTube-fKN6P6xzbPc.mp4')

def test_instagram_photo():
    p = utils.instagram_p("https://www.instagram.com/p/CAoArCNgNvW/").read()
    exp_p = open('./test_file/instagram/pictures/test.jpg', 'rb').read()
    assert p == exp_p

def test_instagram_video():
    v = utils.instagram_v("https://www.instagram.com/p/CAsVLbfAh6O/").read()
    exp_v = open('./test_file/instagram/videos/test.mp4', 'rb').read()
    assert v == exp_v

pytest.main()
