################################################################################
"""
DJ JOE Website Playlist File Generator
--------------------------------------

(c) 2021 - Stanley Solutions - Joe Stanley

This application serves an interface to allow the recording of Apple Music or
Spotify playlists.
"""
################################################################################

# Requirements
import html
from tabulate import tabulate

YOUTUBE_BASE_URL = "https://www.youtube.com/results?search_query={}"

PLAYLIST_HTML = """
    <div>
        <p><h2>Playlist: {playlist}</h2></p>
        {table}
    </div>
"""

def format_youtube_search(terms: list):
    # Generate a search-url for Youtube based on the terms provided.
    query = ' '.join(terms).replace(' ', '%20')
    return YOUTUBE_BASE_URL.format(query)

def playlist_json(tracks):
    """Generate a JSON List of Dictionaries for Each Track."""
    for i, track in enumerate(tracks):
        tracks[i] = {
            "title": track[0],
            "artist": track[1],
            "explicit": track[2],
        }
    return tracks

def playlist_html_table(playlist: str, tracks: str):
    """Generate an HTML Table from the Playlist's Information."""
    table_list = []
    # Search for Text in Tracklist
    for i, track in enumerate(tracks):
        # Apply Hyperlink
        linked_title = f"""<div class="tracktitle"><a href="{format_youtube_search(track[:2])}" target="_blank"
            rel="noopener noreferrer">{track[0]}</a></div>"""
        # Identify Explicit Tracks
        artist_marked_w_explicit = f"""<div class="artist">&nbsp&nbsp&nbsp-&nbsp&nbsp&nbsp{track[1]}</div>"""
        if track[2]:
            artist_marked_w_explicit = f"""<div class="explicit">&nbsp&nbsp&nbsp-&nbsp&nbsp&nbsp{track[1]} (explicit)</div>"""
        table_list.append(
            [linked_title, artist_marked_w_explicit]
        )
    # Generate Table
    table = tabulate(table_list, headers=["Title", "Artist(s)"], tablefmt="unsafehtml")
    # Generate the Inner HTML for the Table
    return PLAYLIST_HTML.format(
        playlist=playlist,
        table=table
    )

# END
