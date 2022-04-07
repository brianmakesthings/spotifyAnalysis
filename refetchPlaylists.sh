python playlist.py waerloga9000 3xHMNdkx6aY5JORnBs4lg3 playlists/brianEDMPlaylist.csv
python playlist.py waerloga9000 7vNQs0SuAd8NTNDu2v9fd4 playlists/brianJPandKRHipHop.csv
python playlist.py Spotify 37i9dQZF1DWZUAeYvs88zc playlists/spotifySadBops.csv
python playlist.py Spotify 37i9dQZF1DX1lVhptIYRda playlists/spotifyHotCountry.csv
python playlist.py Spotify 37i9dQZF1DX4SBhb3fqCJd playlists/spotifyRAndB.csv
python playlist.py Spotify 37i9dQZF1DWXRqgorJj26U playlists/spotifyRockClassics.csv
python playlist.py Spotify 37i9dQZF1DXcRXFNfZr7Tp playlists/spotifyJustHits.csv 
python playlist.py Spotify 37i9dQZF1DXcBWIGoYBM5M playlists/spotifyTopHits.csv 
python playlist.py Spotify 37i9dQZF1DX0XUsuxWHRQd playlists/spotifyRapCaviar.csv 
python playlist.py null 1h0CEZCm6IbFTbxThn6Xcs playlists/premadeClassical.csv
python playlist.py spotify 37i9dQZF1EQn2GRFTFMl2A playlists/90sMix.csv
python playlist.py s4fu8wb8wm4zqumjnssds9ph2 5eE9taMGALspZXJ59p0ERr playlists/MilaJPOP.csv
python playlist.py spotify 37i9dQZF1EQn2GRFTFMl2A playlists/spotifyChristian.csv

for FILE in playlists/*.csv
do
    python lyrics.py $FILE
done
