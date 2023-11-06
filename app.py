import os
from flask import Flask, request, render_template
import requests
import logging

SHOWS_LIST_DEFAULT = ['--DEF--', 'Letterkenny', 'FBOY Island']
MOVIES_LIST_DEFAULT = ['--DEF--', 'Shrek', 'Some Like it Hot', 'Elf']

app_data = {
    'existing_shows': SHOWS_LIST_DEFAULT, 
    'existing_movies': MOVIES_LIST_DEFAULT
}

app = Flask(__name__)

PLEX_ROOT = os.environ['PLEX_ROOT']
QBITTORRENT_HOST = os.environ['QBITTORRENT_HOST']
qbittorrent_creds = dict(
    username=os.environ['QBITTORRENT_USERNAME'],
    password=os.environ['QBITTORRENT_PASSWORD']
    )

@app.route('/', methods=('GET', 'POST'))
def add_new():
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
            urls = torrent_link,
            savepath=path,
            paused='false',
            sequentialDownload='true',
            root_folder='false',
        )
        
        s = requests.session()
        last_request += [('login', s.post(f'{QBITTORRENT_HOST}/api/v2/auth/login', data=qbittorrent_creds).text)]
        last_request += [('add', s.post(f'{QBITTORRENT_HOST}/api/v2/torrents/add', data=req).text)]
        last_request += [('logout', s.post(f'{QBITTORRENT_HOST}/api/v2/auth/logout').text)]
        
        logging.debug(request.form)

    # TODO: Raise error message to user?
    try:
        app_data['existing_shows'] = os.listdir(os.path.join(PLEX_ROOT, 'Media', 'TV Shows'))
        app_data['existing_movies'] = os.listdir(os.path.join(PLEX_ROOT, 'Media', 'Movies'))
    except FileNotFoundError:
        # No-Op, will stay as defaults set at beginning of file
        None
    finally:
        app_data['existing_shows'].sort()
        app_data['existing_movies'].sort()
    
    return render_template('index.html', app_data=app_data, last_request=last_request)
