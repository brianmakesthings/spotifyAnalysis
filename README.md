# spotifyAnalysis

Install Order:

```
$ pip install pandas
$ pip install scikit-learn
$ pip install plotly
$ pip install spotipy
$ pip install swaglyrics
$ pip install nltk
$ pip install wordcloud
$ pip install requests
$ pip install kaleido
```

## Fetch Spotify Playlist Data

#### Run the following files:

```
playlist.py [username] [Spotify playlist ID] [output filename]
```
- username is the user's Spotify user ID
- Spotify playlist ID is the [Spotify ID](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids)
```
lyrics.py [input filename]
genres.py [input filename]
```
- the input file should be a .csv file generated from playlist.py