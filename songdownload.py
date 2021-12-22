from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import re,os

def info(srch, usr):
    songname = srch+" official audio"
    try:
        results = VideosSearch(songname, limit = 1)
    except:
        print("No Internet Error")

    filterwords = {'Official','lyrics', 'lyric', '?','Audio', 'audio', 'Video', 'video', '/','\\','#','HD', 'hd'}

    filtered = lambda toBeFiltered : ' '.join([word for word in toBeFiltered.split() if word not in filterwords]).strip()

    temp = re.sub(r'(!|@|#|~|/|$|\||\"|#|\*|:|/|\?|\\)', '', results.resultComponents[0]['title'])
    title = filtered(temp)
    lst = re.findall('\(.*?\)',title)
    sqlist = re.findall('\[.*?\]',title)
    lst+=sqlist
    newlst = [i for i in lst if ("official" in i.lower() or "audio" in i.lower() or "lyric" in i.lower() and "remix" not in i.lower())]
    for i in newlst:
        title=title.replace(i,"")
 
    title=title.strip()
    url = "https://www.youtube.com/watch?v=" + str(results.resultComponents[0]['id'])

    ydl_opts = {
        'format': 'audio/bestaudio',
        'outtmpl': os.getcwd()+'/static/songs/' + usr + '/' + title+'.%(ext)s',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    path = f'static/songs/{usr}/{title}.mp3'
    return [title, url, path]

