for FILE in ./playlists/*.csv
do
    FILE_NAME=$(basename -- "$FILE")    
    FILE_ROOT="${FILE_NAME%.*}"
    list=$(find recs -type f -name "*$FILE_ROOT*")
    # echo "img/tsne/$FILE_ROOT.png"
    python py_scripts/tsneReduction.py "./img/tsne/$FILE_ROOT" ./spotifydata.csv $FILE $list
done
