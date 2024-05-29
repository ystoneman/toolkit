yt-dlp --flat-playlist --get-id https://www.youtube.com/@YannStoneman | head -n 20 > top_20_video_ids.txt

video_ids=$(<top_20_video_ids.txt)

for video_id in $video_ids
do
    yt --transcript "https://www.youtube.com/watch?v=$video_id" > "${video_id}.txt"
    echo "Transcript for $video_id saved."
done
