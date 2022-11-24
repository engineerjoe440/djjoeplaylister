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
import os, re
from spotipy import Spotify, oauth2

ENV_CLIENT_ID = "SPOTIFY_ID"
ENV_CLIENT_SECRET = "SPOTIFY_SECRET"

TRACKS_PER_PAGE = 20


class SpotifyPlaylister():

    def __init__(self, url: str):
        self.url = url
        # Initialize Spotify Client
        self.spotify_client = Spotify(
            client_credentials_manager=oauth2.SpotifyClientCredentials(
                client_id=os.getenv(ENV_CLIENT_ID),
                client_secret=os.getenv(ENV_CLIENT_SECRET),
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
        result = re.search('playlist/(.*)\?', playlist_url)
        try:
            playlist_uri = result.group(1)
        except:
            playlist_uri = ''
        print("URI:", playlist_uri)
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
        tracklist = []
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
                    tracklist.append(
                        [track_name, track_artists, track_explicit]
                    )
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = self.spotify_client.next(tracks)
            else:
                break
        # Tracklist has been Built
        return playlist_name, tracklist

# END
