#!/bin/bash
# Get Credentials
export SPOTIFY_ID=$(bw get item b0ffba79-cda5-4d83-93e7-af4a0046dae5 | jq -r '.fields[0].value')
export SPOTIFY_SECRET=$(bw get item b0ffba79-cda5-4d83-93e7-af4a0046dae5 | jq -r '.fields[1].value')

# Uncomment this line to see if the Spotify Client Blows up Generically
#python3 test/test_spotify_client.py

pytest