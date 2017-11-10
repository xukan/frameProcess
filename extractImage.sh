#!/bin/bash

path=$(pwd) 
count=0
videos="videos"
frames="frames"
for directory in $(find $path/$videos -mindepth 1 -type d)
do
	#action="`echo "$directory" | rev | cut -d/ -f1 | rev`/"
	action=$(echo $directory | awk -F "/" '{print $NF}')
	#mkdir frames/$action
	mkdir $frames"/"$action
	for videoPath in $(find $directory -type f)
	do
		echo "$video"
		#video contains suffix .avi
		video=$(echo $videoPath | awk -F "/" '{print $NF}')
		videoName=$(echo $video | awk -F"." '{ print $1 }')
		#mkdir frames/$action/$videoName
		#`ffmpeg -i $video frames/$video/image-%03d.jpg`
		#echo "input path is: "$videoPath
		mkdir $frames"/"$action"/"$videoName
		#ffmpeg -i video/walking/person01_walking_d1_uncomp.avi \
			#frames/person01_walking_d1_uncomp/image-%03d.jpg
		`ffmpeg -i $videoPath $frames/$action/$videoName/image-%03d.jpg`
		#let "count++" 
	done
done 
echo "Mission Complete"
