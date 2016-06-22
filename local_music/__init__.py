from media import MediaSkill
from media import mopidy
from adapt.intent import IntentBuilder

import time

import requests

from os.path import dirname
from os import listdir

from mycroft.util.log import getLogger
logger = getLogger(__name__)

__author__ = 'forslund'


class LocalMusic(MediaSkill):
    def __init__(self):
        super(LocalMusic, self).__init__('Local Music')
        self.tracks = None

        url = self.base_conf.get('mopidy_url', None)
        if self.config:
            url = self.config.get('mopidy_url', url)
        self.mopidy = mopidy.Mopidy(url)

        p = self.mopidy.browse('local:directory?type=album')
        albums = {e['name']: e for e in p if e['type'] == 'album'}
        p = self.mopidy.browse('local:directory?type=artist')
        artist = {e['name']: e for e in p if e['type'] == 'artist'}
        p = self.mopidy.browse('local:directory?type=genre')
        genre = {e['name']: e for e in p if e['type'] == 'directory'}
        logger.debug(p)
        self.playlist = {}
        self.playlist.update(genre)
        self.playlist.update(artist)
        self.playlist.update(albums)

    def initialize(self):
        logger.info('initializing Local Music skill')
        super(LocalMusic, self).initialize()
        self.load_data_files(dirname(__file__))

        for p in self.playlist.keys():
            logger.debug("Playlist: " + p)
            self.register_vocabulary(p, 'PlaylistKeyword' + self.name)
        intent = IntentBuilder('PlayPlaylistIntent' + self.name)\
            .require('PlayKeyword')\
            .require('PlaylistKeyword' + self.name)\
            .build()
        self.register_intent(intent, self.handle_play_playlist)
        intent = IntentBuilder('PlayFromIntent' + self.name)\
            .require('PlayKeyword')\
            .require('PlaylistKeyword')\
            .require('FromKeyword')\
            .require('NameKeyword')\
            .build()
        self.register_intent(intent, self.handle_play_playlist)

    def play(self):
        super(LocalMusic, self).play()
        time.sleep(1)
        logger.info(self.mopidy.add_list(self.tracks))
        logger.info(self.mopidy.play())
        self.tracks = None

    def get_available(self, name):
        logger.info(name)
        tracks = None
        if name in self.playlist:
            tracks = self.playlist[name]
        return tracks

    def get_playlist(self, uri):
        tracks = self.mopidy.browse(uri)
        logger.info("uri:")
        logger.info(tracks)
        ret = [t['uri'] for t in tracks if t['type'] == 'track']

        sub_tracks = [t['uri'] for t in tracks if t['type'] != 'track']
        for t in sub_tracks:
            ret = ret + self.get_playlist(t)
        logger.info('found tracks: ' + str(self.tracks))
        return ret

    def handle_play_playlist(self, message):
        p = message.metadata.get('PlaylistKeyword' + self.name)
        self.speak("Playing " + str(p))
        time.sleep(3)
        self.tracks = self.get_playlist(self.playlist[p]['uri'])
        self.play()

    def handle_stop(self, message=None):
        logger.info('Handling stop request')
        self.mopidy.clear_list()
        self.mopidy.stop()
        logger.info("Super")
        super(LocalMusic, self).handle_stop(message)

    def handle_next(self, message):
        self.mopidy.next()

    def handle_prev(self, message):
        self.mopidy.previous()

    def handle_pause(self, message):
        self.mopidy.pause()

    def handle_currently_playing(self, message):
        current_track = self.mopidy.currently_playing()
        if current_track is not None:
            self.mopidy.lower_volume()
            time.sleep(1)
            if 'album' in current_track:
                data = {'current_track': current_track['name'],
                        'artist': current_track['album']['artists'][0]['name']}
                self.speak_dialog('currently_playing', data)
            time.sleep(6)
            self.mopidy.restore_volume()


def create_skill():
    return LocalMusic()
