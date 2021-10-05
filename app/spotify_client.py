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
import os, re, html
from spotipy import Spotify, oauth2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Local Dependencies
from youtube_support import format_youtube_search

ENV_CLIENT_ID = "SPOTIFY_ID"
ENV_CLIENT_SECRET = "SPOTIFY_SECRET"

TRACKS_PER_PAGE = 20


class PlaylistGenerator():

    def __init__(self):
        # Initialize Spotify Client
        self.spotify_client = Spotify(
            client_credentials_manager=oauth2.SpotifyClientCredentials(
                client_id=os.getenv(ENV_CLIENT_ID),
                client_secret=os.getenv(ENV_CLIENT_SECRET),
            )
        )
    
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
    def _tabulate_tracks(self, playlist_url):
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
                    track_explicit = 'Yes' if track['explicit'] else '--'
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
    
    def playlist_basic_pdf(self, url: str):
        """Generate a Simple PDF of the Tracklist."""
        # Capture Tracklist
        playlist, tracks = self._tabulate_tracks(playlist_url=url)
        # Store Table as PDF
        filename = playlist.replace(' ', '_').encode("ascii", "ignore")
        filename = filename.decode('ascii') + '.pdf'
        total_pages = self._num_pages(len(tracks))
        with PdfPages(filename) as pp:
            page_count = 0
            while len(tracks) > 0:
                page_count += 1
                fig_tracks = []
                cell_backgrounds = []
                i = 0
                while i <= TRACKS_PER_PAGE and len(tracks) > 0:
                    track = tracks.pop(0)
                    fig_tracks.append(track[:2])
                    # Manage Cell Coloring
                    if track[-1] == 'Yes':
                        cell_backgrounds.append(['#B86566', '#B86566'])
                    else:
                        cell_backgrounds.append(['w', 'w'])
                    i += 1
                # Generate Table
                plt.figure()
                fig, ax = plt.subplots()
                fig.patch.set_visible(False) # Hide Axes
                ax.set_title(
                    f"{playlist}\n(page {page_count} of {total_pages})"
                )
                ax.axis('off')
                ax.axis('tight')
                # Generate Table
                df = pd.DataFrame(fig_tracks, columns=["Title", "Artist(s)"])
                ax.table(
                    cellText=df.values,
                    colLabels=df.columns,
                    loc="upper center",
                    cellColours=cell_backgrounds,
                )
                fig.set_size_inches([8,10.5])
                fig.tight_layout(rect=[0.11, 0.3, 0.95, .95])
                plt.savefig(pp, format='pdf')
        # Return Path to File
        return os.path.join(os.getcwd(), filename)
    
    def playlist_json(self, url: str):
        """Generate a JSON List of Dictionaries for Each Track."""
        # Capture Tracklist
        playlist, tracks = self._tabulate_tracks(playlist_url=url)
        for i, track in enumerate(tracks):
            tracks[i] = {
                "title": track[0],
                "artist": track[1],
                "explicit": track[2],
            }
        return playlist, tracks
    
    def playlist_html_table(self, url: str, table_id: str = None,
                            classes: str = None):
        """Generate an HTML Table from the Playlist's Information."""
        # Capture Tracklist
        playlist, tracks = self._tabulate_tracks(playlist_url=url)
        table_list = [t[:2] for t in tracks]
        # Generate Table
        df = pd.DataFrame(table_list, columns=["Title", "Artist(s)"])
        # Define Formatter
        def fmtr(text):
            text = html.escape(text)
            # Search for Text in Tracklist
            for i, track in enumerate(tracks):
                # Apply Hyperlink
                if text == track[0]:
                    url = format_youtube_search([text, tracks[i][1]])
                    text = f"""<a href="{url}">{text}</a>"""
                # Identify Explicit Tracks
                if text in track[:2]:
                    if tracks[i][-1] == 'Yes':
                        return f"""<div class="explicit">{text}</div>"""
                    else:
                        return text
            return text
        # Generate the Inner HTML for the Table
        return """
        <div>
            <p><h3>{playlist}</h3></p>
            {table}
        </div>
        """.format(playlist=playlist, table=df.to_html(
            escape=False,
            formatters={
                "Title": fmtr,
                "Artist(s)": fmtr
            },
            table_id=table_id,
            classes=classes,
        ))




if __name__ == '__main__':
    tst_url = "https://open.spotify.com/playlist/3UCaLWJ87hkrrK8laug3vD?fbclid=IwAR38AzTjdxuFOaNshQOyg1lh5oZwIDlMEREnATQBAhtYBzbP815XSLC_NC8"
    playlister = PlaylistGenerator()
    playlister.playlist_basic_pdf(tst_url)
    print(playlister.playlist_html_table(tst_url))