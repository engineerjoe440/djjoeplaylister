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
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Locals
import spotify_client

# Application Base
app = FastAPI()

# Mount the Static File Path
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def page(request: Request, url: str = None):
    """Generate the HTML Page Content Using any Provided Playlist URL"""
    data = ""
    if url != None:
        client = spotify_client.PlaylistGenerator()
        data = client.playlist_html_table(
            url=url,
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