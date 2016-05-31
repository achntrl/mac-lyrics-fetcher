# mac-lyrics-fetcher
Script that fetch lyrics for the song currently playing on iTunes (works on OSX)


## Setup

Requires a client access token from Genius.com: [https://genius.com/api-clients](https://genius.com/api-clients). (Maybe in future will generate authentication from client_id and client_secret.) Add access token credential to "credentials.ini" in project root folder

## Run

`python lyrics.py` while playing a song on iTunes

 I don't think the API have a limitation on the number of hits but just in case lyrics are added in a folder `offline` to avoid fetching them everytime on Genius. Should the Genius html page structure change, we at least have the lyrics of the songs we have already fetched before having to make changes in the script !