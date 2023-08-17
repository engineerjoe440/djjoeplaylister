################################################################################
"""
DJ JOE Website Spotify Playlist File Generator
----------------------------------------------

(c) 2021 - Stanley Solutions - Joe Stanley

This application serves an interface to allow the recording of a Spotify
playlist.
"""
################################################################################

# Requirements
import os
import re
import logging
from spotipy import Spotify, oauth2

CLIENT_ID = os.getenv("SPOTIFY_ID", None)
CLIENT_SECRET = os.getenv("SPOTIFY_SECRET", None)

if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError("Failed to Load API Credentials.")

TRACKS_PER_PAGE = 20

logger = logging.getLogger("uvicorn")

class SpotifyPlaylister:
    """Collector for Spotify Playlists."""

    def __init__(self, url: str):
        self.url = url
        # Initialize Spotify Client
        self.spotify_client = Spotify(
            client_credentials_manager=oauth2.SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )
        )

    def __call__(self):
        return self._tabulate_tracks()

    def _num_pages(self, num_tracks):
        pages = int(num_tracks / TRACKS_PER_PAGE)
        pages += (num_tracks % TRACKS_PER_PAGE > 0)
        return pages

    # Function to Extract Playlist URI from URL
    def _gather_playlist_uri(self, playlist_url):
        result = re.search(r'playlist/(.*)\?', playlist_url)
        if result:
            playlist_uri = result.group(1)
        else:
            playlist_uri = ''
        logger.debug("URI: %s", playlist_uri)
        return playlist_uri

    # Function to Store Playlist Information in Text File
    def _tabulate_tracks(self):
        playlist_url = self.url
        username = 'NA' # Username Doesn't Matter
        results = self.spotify_client.user_playlist(
            username,
            self._gather_playlist_uri(playlist_url),
            fields='tracks,next,name'
        )
        playlist_name = results['name']
        tracks = results['tracks']
        # Generate List of Tracks
        track_list = []
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    # Gather Pertinent Track Information
                    track_name = track['name']
                    track_artists = ""
                    cnt = 0
                    # Gather all Track Artists as Comma-Delimited String
                    for artist in track['artists']:
                        if cnt != 0:
                            track_artists += ', '
                        track_artists += artist['name']
                        cnt += 1
                    # Validate Track Explicit Indicator
                    track_explicit = bool(track['explicit'])
                    # Append Track Information to List
                    track_list.append(
                        [track_name, track_artists, track_explicit]
                    )
                except KeyError:
                    logger.debug(
                        'Skipping track %s by %s (local only?)',
                        track['name'],
                        track['artists'][0]['name']
                    )
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = self.spotify_client.next(tracks)
            else:
                break
        # Track List has been Built
        return playlist_name, track_list

# END
