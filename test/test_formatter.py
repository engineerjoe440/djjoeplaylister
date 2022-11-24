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


from html_formatter import format_youtube_search


@pytest.mark.parametrize('queryterms',[
    ("a", "b", "https://www.youtube.com/results?search_query=a%20b"),
    ("a ", "b", "https://www.youtube.com/results?search_query=a%20%20b"),
])
def test_format_youtube_search(queryterms):
    """Test the Youtube Search Formatter."""
    # Verify that searching all the leading arguments match the last argument.
    assert queryterms[-1] == format_youtube_search(queryterms[:-1])

# END
