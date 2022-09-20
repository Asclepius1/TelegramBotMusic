from __future__ import unicode_literals
import config
import telebot
import youtube_dl
import os

from youtube_search import YoutubeSearch #---------For youtube parser-----------

bot = telebot.TeleBot(config.TOKEN) #-------Bot token-------------
#chat_id = chat.id
def searcher(text): #---------Youtube search func.-------------
    res = YoutubeSearch(text, max_results = 1).to_dict()
    # with open('te.py','w',encoding='utf-8') as r:
    #     r.write(str(res))
    return res

def download(url, title):#---------download video to mp3 func.-------------
    ydl_opts = {
    'outtmpl': title + '.%(ext)s',
    'format': 'bestaudio/best',
    'noplaylist':True,
    #'download_archive': 'music',
    #'progress_hooks':progress(),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Введите название музыки и исполнитель')

@bot.message_handler(content_types=['text'])        
def start(message):
    
    links = searcher(message.text)
    url = None
    for link in links:
        url = "https://www.youtube.com/watch?v="+link['id']
        title = link['title']
    bot.send_message(message.chat.id,  title + " скачивается прошу подождать...")
    download(url,title) #---------Download to hard disk-------------
    bot.send_message(message.chat.id, text="Уже отправляем!")
    bot.send_audio(message.chat.id, audio=open(title + '.mp3', 'rb'))#---------Send audio-------------
    os.remove(title+'.mp3')#---------Delete audio after all -------------
        



#RUN
bot.polling(non_stop=True)
