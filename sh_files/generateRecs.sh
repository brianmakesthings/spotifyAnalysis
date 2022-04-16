for FILE in ./playlists/*.csv
do
    python ./py_scripts/recommendation.py $FILE
done