for FILE in ../playlists/*.csv
do
    FILE_NAME=$(basename -- "$FILE")    
    FILE_ROOT="${FILE_NAME%.*}"
    list=$(find recs -type f -name "*$FILE_ROOT*")
    for rec in $list
    do
        python ../comparePlaylists.py $FILE $rec
    done

done