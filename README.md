Mycroft Media Skills
=====================

### Requirements

These media skills currently requires some external software to work.

- mpg123
- libspotify
- mopidy
- mopidy-spotify
- mopidy-local-mysql

Most of these requirements can be installed through the standard method for the OS. The exception is libspotify that must be retrieved from spotify. For convenience the required software can be installed for debian based distros by running the command

```sh
  sudo ./dev-setup-debian.sh
```

and for red hat based distros 

```
  sudo ./dev-setup-redhat.sh
  ```
  
  should work.
  
### Install skill virtualenv

```
git clone http://github.com/forslund/mycroft-media-skills.git
cd mycroft_media_skills
./setup_skill_container
```

### Mopidy Setup

in *~/.config/mopidy/mopidy.conf* under

`[spotify] `

```
enabled=true
username=USERNAME
password=PASSWORD
```

and under
` [local] `

```
enabled = true
library = sqlite
media_dir = PATH_TO_YOUR_MUSIC
```

after this is done scan the local collection by running

` mopidy local scan `

### Mycroft Setup

Mycroft needs to be pointed to the mopidy server. Add the following to `~/.mycroft/mycroft.ini` for a local mopidy server at the defualt port:

```
[Media]
mopidy_url = http://localhost:6680
```

## Launch the media skills

```
workon mycroft-media-skills

./start.sh
```

## The example skills
**Swedish Radio**
- Swedish radio, a skill to tune in to Swedish radio
examples:

`play p3`
`play p3 from swedish radio`

**spotify**
- a skill to play music from spotify. the skill collects the play lists from the user and will play them if requested. If the spotify skill is specified explicitly it also performs an album search
examples:

`play discover weekly`
`play hello nasty from spotify`

**local music**
- the local music skill browses the local media directory and adds each artist, album and genre found as a play intent.

examples:

`play Armikrog OST`

`play something by Terry Scott Taylor`

`play rock music`
