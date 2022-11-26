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
import pytest

BASE = str(Path(__file__).parent.parent / "app")

sys.path.insert(0, BASE)


from apple_music_client import ApplePlaylister


@pytest.mark.skip
def test_client_doesnt_crash():
    """Just make sure the Spotify Client doesn't die."""
    playlister = ApplePlaylister(url=(
        "https://music.apple.com/us/playlist/todays-hits/pl.f4d106fed2bd41149aa"
        + "acabb233eb5eb"
    ))
    print(playlister())

# END
