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

class ApplePlaylister():

    def __init__(self, url):
        self.url = url
    
    def __call__(self):
        return self._tabulate_tracks()

    def _get_creds(self):
        headers = {
            'Accept': (
                'text/html,application/xhtml+xml,application/xml;'
                'q=0.9,*/*;q=0.8'
            ),
            'Host': 'music.apple.com',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 '
                'Safari/605.1.15'
            ),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        response = requests.get(self.url, headers=headers)
        html = response.text
        webpage = BeautifulSoup(html, "html.parser")
        raw = webpage.find_all("meta",
            attrs={"name":"desktop-music-app/config/environment"})[0].get(
                "content"
            )
        clean = unquote(raw)
        dictifyed = json.loads(clean)
        data = dictifyed["MEDIA_API"]["token"]
        return data

    def _extract_url_data(self):
        array = self.url.split("/")
        country = array[3]
        playlist_id = array[6]
        return country, playlist_id

    def _get_data(self, country, playlist_id, token):
        headers = {
            'Accept': '*/*',
            'Origin': 'music.apple.com',
            'Referer': 'music.apple.com',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'amp-api.music.apple.com',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 '
                'Safari/605.1.15'
            ),
            'Authorization': f"Bearer {token}",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }
        params = (
            ('l', 'en-us'),
        )
        url = APPLE_MUSIC_REQUEST.format(
            country=country,
            playlist_id=playlist_id,
        )
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def _tabulate_tracks(self):
        # Load the Playlist Data
        creds = self._get_creds()
        country, playlist_id = self._extract_url_data()
        jsondata = self._get_data(country, playlist_id, creds)
        track_data = jsondata['data']
        # Iteratively Create Track Lists
        tracks = []
        for track_data_set in track_data:
            attributes = track_data_set['attributes']
            title = attributes['name']
            artist = attributes['artistName']
            explicit = attributes.get('contentRating', '') == 'explicit'
            tracks.append([title, artist, explicit])
        return '', tracks



if __name__ == '__main__':
    tst_url = "https://music.apple.com/us/playlist/todays-hits/pl.f4d106fed2bd41149aaacabb233eb5eb"
    playlister = ApplePlaylister(url=tst_url)
    print(playlister())