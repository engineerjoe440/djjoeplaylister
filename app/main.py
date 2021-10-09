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
from urllib.parse import urlparse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Locals
import spotify_client
import apple_music_client
from formatter import playlist_html_table

# Application Base
app = FastAPI()

# Mount the Static File Path
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def page(request: Request, url: str = None):
    """Generate the HTML Page Content Using any Provided Playlist URL"""
    data = ""
    if url != None:
        # "Switch" On Domain Name
        domain = urlparse(url).netloc
        if 'music.apple' in domain:
            client = apple_music_client.ApplePlaylister(url)
        elif 'spotify' in domain:
            client = spotify_client.SpotifyPlaylister(url)
        playlist, tracks = client()
        data = playlist_html_table(
            playlist=playlist,
            tracks=tracks,
            table_id="playlist",
            classes="",
        )
    # Return Template Response Using Data
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "playlist_table": data,
        },
    )

# Main Application Response
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return page(request=request)

# Load Playlist
@app.post("/load_playlist", response_class=HTMLResponse)
async def load_playlist(request: Request, playlist: str = Form(...)):
    print(playlist)
    return page(request=request, url=playlist)