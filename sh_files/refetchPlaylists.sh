python ./py_scripts/playlist.py waerloga9000 3xHMNdkx6aY5JORnBs4lg3 ./playlists/brianEDMPlaylist.csv
python ./py_scripts/playlist.py waerloga9000 7vNQs0SuAd8NTNDu2v9fd4 ./playlists/brianJPandKRHipHop.csv
python ./py_scripts/playlist.py Spotify 37i9dQZF1DWZUAeYvs88zc ./playlists/spotifySadBops.csv
python ./py_scripts/playlist.py Spotify 37i9dQZF1DX1lVhptIYRda ./playlists/spotifyHotCountry.csv
python ./py_scripts/playlist.py Spotify 37i9dQZF1DX4SBhb3fqCJd ./playlists/spotifyRAndB.csv
python ./py_scripts/playlist.py Spotify 37i9dQZF1DWXRqgorJj26U ./playlists/spotifyRockClassics.csv
python ./py_scripts/playlist.py Spotify 37i9dQZF1DXcRXFNfZr7Tp ./playlists/spotifyJustHits.csv 
python ./py_scripts/playlist.py Spotify 37i9dQZF1DXcBWIGoYBM5M ./playlists/spotifyTopHits.csv 
python ./py_scripts/playlist.py Spotify 37i9dQZF1DX0XUsuxWHRQd ./playlists/spotifyRapCaviar.csv 
python ./py_scripts/playlist.py null 1h0CEZCm6IbFTbxThn6Xcs ./playlists/premadeClassical.csv
python ./py_scripts/playlist.py spotify 37i9dQZF1EQn2GRFTFMl2A ./playlists/90sMix.csv
python ./py_scripts/playlist.py s4fu8wb8wm4zqumjnssds9ph2 5eE9taMGALspZXJ59p0ERr ./playlists/MilaJPOP.csv
python ./py_scripts/playlist.py spotify 0NABnUOcrFIWP27uXedhi6 ./playlists/spotifyChristian.csv

for FILE in ./playlists/*.csv
do
    python ./py_scripts/lyrics.py $FILE
    python ./py_scripts/mood.py $FILE
done
