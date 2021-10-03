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
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Application Base
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 

# Main Application Response
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "fastapi_token": "Hello World"
        },
    )