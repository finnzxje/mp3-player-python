from Playlist import Playlist
from AudioEngine import AudioEngine
from Track import Track
from tkinter import filedialog
from tkinter import *

import json

class MusicPlayer:

    def __init__(self):
        """
        Initialize the MusicPlayer class
        """
        self.current_track = None
        self.playlist = Playlist()
        self.audio_engine = AudioEngine()
        self.is_playing = False
        self.volume = 0.5
        self.current_position = 0
        self.index = 0

    def remove_track(self):
        self.current_position = 0
        self.index = 0
        self.current_track = None

    def add_track_from_files(self, file_paths):
        """
        Add tracks from files to the playlist
        """
        existed_tracks = [track.get_path() for track in self.playlist.get_tracks()]
        for file_path in file_paths:
            if file_path not in existed_tracks:
                track = Track(file_path)
                self.playlist.add_track(track)

    def play(self):
        """
        Play the current track  (it's can be random song or first to end song of folder)
        """
        self.current_position = 0
        if len(self.playlist) == 0:
            return
        self.current_track = self.playlist.tracks[self.index]
        self.audio_engine.load_audio(self.current_track.get_path())
        self.audio_engine.start_playback()
        self.is_playing = True

    def on_loop(self):
        """
        Fuction loop
        """
        self.audio_engine.start_loop()

    def play_at_index(self, index):
        """
        Play the track at the given index
        :param index:
        :return:
        """
        self.index = index
        self.play()

    def pause(self):
        """
        Pause the current track
        """
        self.audio_engine.pause_playback(self.is_playing)
        self.is_playing = not self.is_playing

    def stop(self):
        """
        Stop the current track
        """
        self.current_track = None
        self.audio_engine.stop_playback()
        self.is_playing = False

    def next_track(self):
        """
        Skip to the next track
        """
        self.index = (self.index + 1) % len(self.playlist)
        self.current_track = self.playlist.tracks[self.index]
        self.play()

    def previous_track(self):
        """
        Skip to the previous track
        """
        self.index = (self.index - 1) % len(self.playlist)
        self.current_track = self.playlist.tracks[self.index]
        self.play()

    def shuffle_playlist(self):
        """
        Shuffle the playlist
        """
        if not self.playlist:
            print("Playlist is empty")
            return
        self.index = 0
        self.playlist.shuffle()
        self.current_track = self.playlist.tracks[self.index]

    def set_volume(self, volume):
        """
        Set the volume
        """
        self.volume = volume
        self.audio_engine.set_volume(volume)

    def mute(self):
        """
        Mute the volume
        """
        self.audio_engine.mute_unmute()

    def seek(self, position):
        """
        Seek to a specific position
        """
        self.current_position = position * 1000
        self.audio_engine.seek(position)

    def get_position(self):
        """
        Get the current position of the song
        """

        return self.current_position + self.audio_engine.get_position()

    def add_to_playlist(self, track):
        """"
        Add a track to playlist
        """
        self.playlist.add_track(track)

    def remove_from_playlist(self, track):
        """"
        Remove a track from playlist
        """

        self.playlist.remove_track(track)

    def get_current_track(self):
        """"
        Get the current playing track
        """

        return self.playlist.get_track(self.index)

    def get_all_tracks(self):
        """"
        Get all tracks in the playlist
        """

        return self.playlist.get_tracks()

    def get_duration(self):
        """"
        Get the duration of the current track
        """

        return self.playlist.get_track(self.index).get_duration()

    def is_ended(self):
        """
        Check if the song is over yet
        :return:
        """
        if self.audio_engine.get_position() < 0:
            self.current_position = 0
            return True
        else:
            return False
    def set_all_playlist(self):
        return self.playlist.tracks()
    

    
    #setting autoplay 
    
    def get_setting(self, setting: str):
        """
        Lấy cài đặt từ file cấu hình JSON.

        Args:
            setting (str): Tên cài đặt cần lấy.

        Returns:
            str: Giá trị của cài đặt, hoặc 'false' nếu không tìm thấy.
        """
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
            return data.get(setting, 'false')  
        except FileNotFoundError:
            return 'false'        
    def save_setting(self, setting: str, value: str):
        """
        Lưu cài đặt vào file cấu hình JSON.

        Args:
            setting (str): Tên cài đặt cần lưu.
            value (str): Giá trị của cài đặt cần lưu.
        """
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[setting] = value  

        with open("config.json", "w") as f:
            json.dump(data, f, indent=4) 

if __name__ == "__main__":
    """
    Test the MusicPlayer class
    """
    tk = Tk()
    music_player = MusicPlayer()
    #    music_player.add_track_from_files(["C:\\Users\\LENOVO\\Desktop\\TEFLON DON.mp3"])
    while True:
        print("Enter 1 for playing")
        print("Enter 2 for pausing")
        print("Enter 3 for stopping")
        print("Enter 4 for next track")
        print("Enter 5 for previous track")
        print("Enter 6 for shuffle playlist")
        print("Enter 7 for set volume")
        print("Enter 8 for mute/unmute")
        print("Enter 9 for seek")
        print("Enter 10 to exit")
        print("Enter 11 to add track(s) from file(s)")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            music_player.play()
        elif choice == 2:
            music_player.pause()
        elif choice == 3:
            music_player.stop()
        elif choice == 4:
            music_player.next_track()
        elif choice == 5:
            music_player.previous_track()
        elif choice == 6:
            music_player.shuffle_playlist()
        elif choice == 7:
            t_volume = float(input("Enter the volume: "))
            music_player.set_volume(t_volume)
        elif choice == 8:
            music_player.mute()
        elif choice == 9:
            position = int(input("Enter the position: "))
            music_player.seek(position)
        elif choice == 10:
            exit(0)
        elif choice == 11:
            file_paths = filedialog.askopenfilenames(initialdir='C:/Users/LENOVO/Desktop',
                                                     title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
            music_player.add_track_from_files(file_paths)
        else:
            print("Invalid choice")