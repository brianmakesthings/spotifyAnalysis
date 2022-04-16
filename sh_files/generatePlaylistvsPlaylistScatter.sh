# https://superuser.com/questions/318067/how-to-iterate-over-all-pair-combinations-in-a-list-in-bash
# create pairwise comparisons
set -- ./playlists/*.csv
for a; do
    A_FILE_NAME=$(basename -- "$a")    
    A_FILE_ROOT="${A_FILE_NAME%.*}"
    shift
    for b; do
        B_FILE_NAME=$(basename -- "$b")    
        B_FILE_ROOT="${B_FILE_NAME%.*}"
        # echo $B_FILE_ROOT
        python ./py_scripts/scatterplotMatrix.py $a $b "$A_FILE_ROOT vs $B_FILE_ROOT Scatterplot Matrix" "playlistVsPlaylist/"
    done
done