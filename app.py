import os
from flask import Flask, request
from flask import render_template
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

PLEX_ROOT = os.environ['PLEX_ROOT']
QBITTORRENT_HOST_ROOT = 'https://qbittorrent.agar-agaria.com'
qbittorrent_creds = dict(
    username=os.environ['QBITTORRENT_USERNAME'],
    password=os.environ['QBITTORRENT_PASSWORD']
    )

@app.route('/', methods=('GET', 'POST'))
def hello_world():
    last_request = None
    if request.method == 'POST':
        torrent_link = request.form['magnet_link']
        media_type = request.form['type']
        media_name = request.form['media_name']
        custom_name = request.form['custom_name']
        season = request.form['season']

        if media_type == 'tv':
            path = os.path.join(PLEX_ROOT, 'Media', 'TV Shows', media_name if media_name != 'custom' else custom_name, f'Season {season}')
        else:
            path = os.path.join(PLEX_ROOT, 'Media', 'Movies', media_name if media_name != 'custom' else custom_name)
        last_request = ['adding:', torrent_link, 'to:', path]
        
        req = dict(
            savepath=path,
            paused='false',
            sequentialDownload='true',
            root_folder='false',
            urls = torrent_link
        )
        
        s = requests.session()
        r = s.post(f'{QBITTORRENT_HOST_ROOT}/api/v2/auth/login', data=qbittorrent_creds)
        print(r.text)
        last_request += [('login', r.text)]
        r = s.post(f'{QBITTORRENT_HOST_ROOT}/api/v2/torrents/add', data=req)
        last_request += [('add', r.text)]
        r = s.post(f'{QBITTORRENT_HOST_ROOT}/api/v2/auth/logout')
        print(r.text)
        last_request += [('logout', r.text)]
        

    existing_shows = os.listdir(os.path.join(PLEX_ROOT, 'Media', 'TV Shows'))
    existing_movies = os.listdir(os.path.join(PLEX_ROOT, 'Media', 'Movies'))
    return render_template('index.html', existing_shows=existing_shows+existing_movies, last_request=last_request)