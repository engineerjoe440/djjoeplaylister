################################################################################
"""
DJ JOE Website Spotify Playlist File Generator
----------------------------------------------

(c) 2021 - Stanley Solutions - Joe Stanley

This application serves an interface to allow the recording of a Spotify
playlist.
"""
################################################################################


YOUTUBE_BASE_URL = "https://www.youtube.com/results?search_query={}"

def format_youtube_search(terms: list):
    # Generate a search-url for Youtube based on the terms provided.
    query = ' '.join(terms).replace(' ', '%20')
    return YOUTUBE_BASE_URL.format(query)