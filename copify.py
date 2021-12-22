import shutil, requests
from typing import cast
from flask import Flask, render_template, url_for, request, redirect
from yt_dlp.compat import compat_ctypes_WINFUNCTYPE
from songdownload import info
import os
import atexit, base64
from apscheduler.schedulers.background import BackgroundScheduler
from timelydeleter import deleter

scheduler = BackgroundScheduler()
scheduler.add_job(func=deleter, trigger="interval", seconds=300)
scheduler.start()

def refresh():
    temp = {}
    if os.listdir("static/songs"):
        for ip in os.listdir("static/songs"):
            current_songs = os.listdir(f"static/songs/{ip}")
            if current_songs[-1]:
                temp.update({ip: f'static/songs/{ip}/{current_songs[-1]}'})
    return temp

app = Flask(__name__)
url_hit = "https://api.countapi.xyz/hit/shubh/28d7d3f5-8ef2-4c18-a01f-4c482021b1cb"
url_view = "https://api.countapi.xyz/get/shubh/28d7d3f5-8ef2-4c18-a01f-4c482021b1cb"

def increment_count(url):
    temp = requests.get(url)
    del (temp)


def get_current_count(url):
    response = eval(requests.get(url).text)['value']
    return f'{response:,}'


@app.route("/", methods = ['GET', 'POST'])
def play():
    songs = refresh()
    usr = str(base64.standard_b64encode(request.remote_addr.encode()).decode())
    if request.method == "POST":
        print("Current path: "+os.getcwd())
        results = info(str(request.form["name"]), usr)
        if usr not in songs.keys():
            songs.update({usr: results[2]})
        else:
            if songs[usr] == results[2]:
                print("Same song")
                pass
            else:
                os.remove(songs[usr])
                songs[usr] = results[2]
        increment_count(url_hit)
        return render_template("play.html", addr=usr, path=results[2], o_name=results[0],
                               count=get_current_count(url_view))
    else:
        if usr in songs.keys():
            print(f"{usr} already in list, deleting previous files.")
            path = os.path.join("static/songs/", usr)
            shutil.rmtree(path)
            songs = refresh()
        return render_template("play.html", count=get_current_count(url_view))

@app.route("/tandc")
def root():
    return render_template('Terms of Service.html')


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    songs = refresh()
    app.run(host='0.0.0.0', port=80)
    #app.run(debug=True)
