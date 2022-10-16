# djjoespotifyplaylister
*A web-based tool to automatically consume Spotify and Apple Music playlists into a*
*Youtube-searchable and printable format, showing just the right ammount of info for*
*DJs with time constraints!*

### Inspiration
As a mobile DJ, I often am provided "playlists" in various forms: Word documents, text
files, quickly-scribbled hand-written notes, Spotify playlists, and Apple Music playlists.

It quickly became apparent for me, that I spent *way* more time working through these
Spotify playlists and Apple Music playlists to get them into a form that was actually
helpful for me. In most cases, I could not simply copy/paste the Spotify list(s) out so
that I could search for the songs of interest in my own library and then determine whether
I'd need to aqcuire additional music. Thus... I came to the conclusion, I'd want a little
assistance from my computer.

### Stages of Development
I originally started with a simple Tkinter-app that used the [`spotipy`](https://spotipy.readthedocs.io/en/latest/)
package to pull playlist information into a simple plain-text file. It was helpful, but
ended up incurring a few additional challenges of its own. The largest of which being the
fact I had to securly pass the API secrets around with the script itself. This became a
real burden, so I decided to enhance the system into a full-service mini web-app that
could be utilized for exactly this purpose. The web-app could run persistently on a server
that could hang on to those secrets and allow me to access the tool from anywhere.

Thus, the `djjoeplaylister` was born.

### Technical Details
This app is built on the shoulders of giants, so let me give credit to those where it's due!

**Technology Specs**
* Language: Python 3
* Web Framework: [FastAPI](https://fastapi.tiangolo.com/)
* Web Listener/ASGI Server: [Uvicorn](https://uvicorn.org/)
* Reverse Proxy: [Nginx](https://nginx.com/)
* Hosting Provider: [Linode virtual hosting](https://linode.com/)
* Operating System: Ubuntu server
* App Deployment Enviromnent: Dockerized Container

**Python Packages Leveraged**
* Spotify Client: [`spotipy`](https://spotipy.readthedocs.io/en/latest/)
* Apple Music Client: [`requests`](https://docs.python-requests.org/en/latest/)
* HTML Table Generation: [`pandas`]()

Additionally, I'd like to provide a special thanks and shout-out to this gist that
helped me get up and running with consuming the Apple Music playlist without dealing
with Apple's crummy developer program ($99 dolars a year, just to access an API? No
thank you!) https://gist.github.com/aleclol/ef9e87d0964f00975f82d5373a814447

------

## Deploying
1. Clone/Pull repo contents down to server
2. Verify installation of Nginx/Docker/docker-compose
3. Configure Nginx to route to the container
4. Configure the required environment variables for Spotipy in a `.env` file:
  * `SPOTIFY_ID=<api-id>`
  * `SPOTIFY_SECRET=<api-key>`
5. Run Docker container with docker-compose
  * `docker-compose up -d --build`