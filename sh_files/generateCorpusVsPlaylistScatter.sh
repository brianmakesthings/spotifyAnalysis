for FILE in ./playlists/*.csv
do
    FILE_NAME=$(basename -- "$FILE")    
    FILE_ROOT="${FILE_NAME%.*}"
    # list=$(find recs -type f -name "*$FILE_ROOT*")
    # echo "img/tsne/$FILE_ROOT.png"
    python py_scripts/scatterplotMatrix.py ./spotifydata.csv $FILE "Corpus vs $FILE_ROOT Scatterplot Matrix" "playlistVsCorpus/"
done