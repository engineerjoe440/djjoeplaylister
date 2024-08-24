################################################################################
"""
DJ JOE Website Apple Music Playlist File Generator
--------------------------------------------------

(c) 2021 - Stanley Solutions - Joe Stanley

This application serves an interface to allow the recording of a Apple Music
playlist.
"""
################################################################################

# Requirements
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json

APPLE_MUSIC_REQUEST = (
    "https://amp-api.music.apple.com/v1/catalog/{country}/playlists/"
    "{playlist_id}/tracks"
)

class ApplePlaylister:

    def __init__(self, url):
        self.url = url

    def __call__(self):
        return self._tabulate_tracks()

    def _tabulate_tracks(self):
        track_list = []
        # Load the Playlist Page
        response = requests.get(self.url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for meta in soup.find_all('meta', attrs={"property": "music:song"}):
            link = meta.get('content')
            # Load Each Song's Page -- This will take some time -- await?
            song_soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            # Get Specific Data
            title = song_soup.find('h1', attrs={"data-testid": "song-title"})
            explicit = title.find('span', attrs={"data-testid": "explicit-badge"})
            artist = song_soup.find('span', attrs={"data-testid": "song-subtitle-artist-link0"})
            track_list.append(
                [str(title.text), str(artist.text), bool(explicit)]
            )

        return '', track_list

# END
