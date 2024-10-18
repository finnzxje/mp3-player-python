import pygame
from tkinter import *
from tkinter import filedialog


class AudioEngine:
    def __init__(self):
        pygame.mixer.init()
        self.current_audio = None  # Placeholder for storing the current audio file
        self.last_volume = 1.0  # Store audio before muting
        pygame.mixer.music.set_volume(0.5)  # Set initial volume to 50%
        self.audio_files = []  # List to store the full paths of audio files

    def load_audio(self, current_audio):
        """"
        Function to load a single audio file
        """
        self.current_audio = current_audio
        pygame.mixer.music.load(current_audio)

    def start_playback(self):
        """"
        Function to start the music
        """
        pygame.mixer.music.play()

    def stop_playback(self):
        """"
        Function to stop the music
        """
        pygame.mixer.music.stop()

    def pause_playback(self, action):
        """"
        Function to pause and unpause the music
        """
        if action:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def mute_unmute(self):
        """"
        Function to turn on or off the volume
        """
        if pygame.mixer.music.get_volume() > 0:
            self.last_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.last_volume)

    def set_volume(self, volume):
        """"
        Function to set the volume
        """
        pygame.mixer.music.set_volume(volume)

    def seek(self, position):
        """"
        Function to seek to a specific position
        """
        pygame.mixer.music.play(loops=0, start=position)

    def get_position(self):
        """
        Get the current position of the song
        """

        return pygame.mixer.music.get_pos()


# Ham main test thoi
if __name__ == '__main__':
    # Initialize pygame mixer
    # Initialize the main window
    root = Tk()
    root.title('MP3-Player')
    root.geometry("500x400")

    # Create the listbox to display songs
    song_box = Listbox(root, bg='black', fg='green', width=60, selectbackground='gray', selectforeground='black')
    song_box.pack(pady=20)

    # Instantiate the AudioEngine class
    audio_engine = AudioEngine()

    # Create the menu bar
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Add songs menu
    add_song_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label='Add Songs', menu=add_song_menu)


    def add_song():
        """Add a single song to the playlist."""
        current_audio = filedialog.askopenfilename(title='Choose a song', filetypes=(('MP3 Files', '*.mp3'),))
        if current_audio:
            audio_engine.audio_files.append(current_audio)  # Append the selected file to the audio list
            song_box.insert(END, audio_engine.load_audio(current_audio))  # Insert the song name into the listbox


    def add_many_songs():
        """Add multiple songs to the playlist."""
        songs = filedialog.askopenfilenames(title='Choose songs', filetypes=(('MP3 Files', '*.mp3'),))
        for song in songs:
            audio_engine.audio_files.append(song)  # Append each file to the audio list
            song_box.insert(END, audio_engine.load_audio(song))  # Insert each song name into the listbox


    # Add commands to the menu
    add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
    add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

    # Create a control frame for buttons
    control_frame = Frame(root)
    control_frame.pack(pady=20)

    # Create buttons to start and pause the song
    play_button = Button(control_frame, text="Play Song", command=audio_engine.start_playback)
    play_button.grid(row=0, column=0, padx=10)


    def stop():
        audio_engine.stop_playback()
        song_box.select_clear(ACTIVE)


    # Create a pause/resume button
    pause_button = Button(control_frame, text="Stop", command=stop)
    pause_button.grid(row=0, column=1, padx=10)

    # Create a Mute/Unmute button
    mute_button = Button(control_frame, text="Mute", command=audio_engine.mute_unmute)
    mute_button.grid(row=0, column=7, padx=5)

    # Create a volume control scale
    volume_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=audio_engine.set_volume, label="Volume")
    volume_slider.set(50)  # Set initial volume to 50%
    volume_slider.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()
