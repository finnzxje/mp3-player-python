import random
from Track import Track
from tkinter import filedialog
from tkinter import *


class Playlist:
    def __init__(self):
        """"
        Initialize the Playlist class
        """
        self.tracks = []

    def add_track(self, track):
        """"
        Add a track to the playlist
        """
        self.tracks.append(track)

    def remove_track(self, track):
        """"
        Remove a track from the playlist
        """
        self.tracks.remove(track)

    def get_tracks(self):
        """"
        Get all tracks in the playlist
        """
        return self.tracks

    def shuffle(self):
        """"
        Shuffle the tracks in the playlist
        """
        random.shuffle(self.tracks)

    def __len__(self):
        """"
        Get the number of tracks in the playlist
        """
        return len(self.tracks)

    def get_track(self, position):
        return self.tracks[position]


if __name__ == "__main__":
    """"
    Test the Playlist class
    """
    Tk = Tk()
    test = Playlist()
    while True:
        print("Enter 1 for adding a track")
        print("Enter 2 for removing a track")
        print("Enter 3 for getting all tracks")
        print("Enter 4 for shuffling the tracks")
        print("Enter 5 to exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            file_track = filedialog.askopenfilename(initialdir='C:/Users/LENOVO/Desktop',
                                                    title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
            test.add_track(file_track)
        elif choice == 2:
            file_track = Track(input("Enter the file path of the track: "))
            test.remove_track(file_track)
        elif choice == 3:
            print(test.get_tracks())
        elif choice == 4:
            test.shuffle()
        elif choice == 5:
            break
        else:
            print("Invalid choice")
