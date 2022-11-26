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
        "https://open.spotify.com/playlist/3KHb0WRmzbp9WH7E2mXVmx?si=fa8f7abb94d74345"
    ))
    print(playlister())


if __name__ == "__main__":
    test_client_doesnt_crash()

# END
