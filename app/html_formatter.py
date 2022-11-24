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
import pandas as pd

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

def playlist_html_table(playlist: str, tracks: str, table_id: str = None,
                        classes: str = None):
    """Generate an HTML Table from the Playlist's Information."""
    table_list = [t[:2] for t in tracks]
    # Generate Table
    df = pd.DataFrame(table_list, columns=["Title", "Artist(s)"])
    # Define Formatter
    def formatter(text):
        text = html.escape(text)
        # Search for Text in Tracklist
        for i, track in enumerate(tracks):
            # Apply Hyperlink
            if text == html.escape(track[0]):
                url = format_youtube_search([text, tracks[i][1]])
                text = f"""<a href="{url}" target="_blank"
                    rel="noopener noreferrer">{text}</a>"""
            # Identify Explicit Tracks
            if text in track[:2]:
                if tracks[i][-1]:
                    return f"""<div class="explicit">{text} (explicit)</div>"""
                else:
                    return text
        return text
    # Generate the Inner HTML for the Table
    return PLAYLIST_HTML.format(playlist=playlist, table=df.to_html(
        escape=False,
        formatters={
            "Title": formatter,
            "Artist(s)": formatter
        },
        index=False,
        table_id=table_id,
        classes=classes,
    ))

# END
