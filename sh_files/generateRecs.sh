for FILE in ../playlists/*.csv
do
    python ../recommendation.py $FILE
done