this small flask app helps you add torrents to a qbittorrent server running on a plex host.

run [waitress_serv.py](./waitress_serve.py) to start the server, in there you can change the host/port that is used (default `0.0.0.0:50627`)

the following environment variables must be set:
- `PLEX_ROOT` (the root folder for your plex files)
- `QBITTORRENT_HOST` (eg: `https://qbittorrent.example.com`)
- `QBITTORRENT_USERNAME`
- `QBITTORRENT_PASSWORD`
