import sys
sys.dont_write_bytecode = True

import wasabi2d as w2d
import wasabi2d.music as w2d_music
import os
import random
import copy

class MusicPlayer:
    def __init__(self, music_folder="Music"):
        self.music_folder = music_folder
        self.playlist = []
        self.current_track_index = -1
        self.is_playing = False
        self.load_music_files()

    def load_music_files(self):
        if not os.path.exists(self.music_folder):
            # print(f"Music folder '{self.music_folder}' does not exist.")
            return
        files = [f for f in os.listdir(self.music_folder) if f.lower().endswith(".ogg")]
        self.playlist = [f.lower() for f in files]
        for i in range(100):
            self.playlist.append(copy.copy(self.playlist[0]))
        random.shuffle(self.playlist)

    def play_next(self):
        if not self.playlist:
            return
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        track = self.playlist[self.current_track_index]
        # print(f"Playing track: {track}")
        w2d_music.play_once(track)
        self.is_playing = True

    def check_music(self):
        # Check if music is playing, if not play next
        if not w2d_music.is_playing(None):
            self.play_next()

    def start(self):
        if not self.playlist:
            # print("Playlist is empty, cannot start music.")
            return
        self.current_track_index = -1
        self.play_next()
        # Schedule periodic check every 1 second
        w2d.clock.schedule(self.check_music, 1.0)
