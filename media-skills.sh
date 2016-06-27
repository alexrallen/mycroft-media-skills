#! /usr/bin/env bash

function usage {
  echo
  echo "Quickly start, stop or restart the media skills in detached screens"
  echo
  echo "usage: $0 [-h] (start|stop|restart)"
  echo "      -h             this help message"
  echo "      start          starts mopidy and the media skills"
  echo "      stop           stops media skills and mopidy"
  echo "      restart        restarts mopidy and media skills"
  echo
  echo "screen tips:"
  echo "            run 'screen -list' to see all running screens"
  echo "            run 'screen -r <screen-name>' (e.g. 'screen -r mycroft-service') to reatach a screen"
  echo "            press ctrl + a, ctrl + d to detace the screen again"
  echo "            See the screen man page for more details"
  echo
}


function start-media-skills {
  echo "Starting mopidy"
  screen -mdS media-skills-mopidy mopidy --config=~/.config/mopidy/mopidy.conf:mopidy.conf
  sleep 15
  screen -mdS media-skills-spotify mycroft-skill-container ./spotify
  screen -mdS media-skills-local-music mycroft-skill-container ./local_music
  screen -mdS media-skills-swedish-radio mycroft-skill-container ./swedishradio
  screen -mdS media-skills-gmusic mycroft-skill-container ./gmusic
}

function stop-media-skills {
  screen -XS media-skills-spotify quit
  screen -XS media-skills-local-music quit
  screen -XS media-skills-swedish-radio quit
  screen -XS media-skills-gmusic quit
  screen -XS media-skills-mopidy quit
}


if [[ -z "$1" || "$1" == "-h" ]]
then
  usage
  exit 1
elif [ "$1" == "start" ]
then
  start-media-skills
  echo "Media skills started"
  exit 0
elif [ "$1" == "stop" ]
then
  stop-media-skills
  echo "Media skills stopped"
  exit 0
elif [ "$1" == "restart" ]
then
  stop-media-skills
  echo "Stopping Media skills"
  start-media-skills
  echo "Media skills restarted"
  exit 0
else
  usage
  exit 1
fi

