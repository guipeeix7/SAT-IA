search_dir=./input
for entry in "$search_dir"/*.desc
do
    echo $entry
    python teFGA.py $entry
done
