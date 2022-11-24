################################################################################
"""
DJ JOE Website Playlist File Generator
--------------------------------------

(c) 2021 - Stanley Solutions - Joe Stanley

This application serves an interface to allow the recording of Apple Music or
Spotify playlists.
"""
################################################################################

import sys
from pathlib import Path

BASE = str(Path(__file__).parent.parent / "app")

sys.path.insert(0, BASE)


from spotify_client import SpotifyPlaylister


def test_client_doesnt_crash():
    """Just make sure the Spotify Client doesn't die."""
    playlister = SpotifyPlaylister(url=(
        "https://open.spotify.com/playlist/3UCaLWJ87hkrrK8laug3vD?fbclid=IwAR38"
        + "AzTjdxuFOaNshQOyg1lh5oZwIDlMEREnATQBAhtYBzbP815XSLC_NC8"
    ))
    print(playlister())

# END
