import pygame
from tkinter import *
from tkinter import filedialog

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the main window : khoi tao cua so
root = Tk()
root.title('MP3-Player')
root.geometry("500x400")

# Define the AudioEngine class : xac dinh lop
class AudioEngine:
    def __init__(self):
        self.current_audio = None  # Placeholder for storing the current audio file : luu tru duong dan cua file dang phat nhac
        self.paused = False  # To track whether the music is paused : theo doi trang thai tam ngung
        self.last_volume = 1.0 # Store audio before muting : luu tru am thanh truoc khi tat tieng
        pygame.mixer.music.set_volume(0.5)  # Set initial volume to 50% : gia tri mac dinh cua am luong
        self.audio_files = []  # List to store the full paths of audio files :danh sach chua duong dan cua cac file

    def one_load_audio(self):
        """"
        Function to load a single audio file
        Allow the user to select any .mp3 file from any directory
        """
        self.current_audio = filedialog.askopenfilename(title='Choose a song', filetypes=(('MP3 Files', '*.mp3'),))
        if self.current_audio:
            # Extract just the filename without the path and extension
            song = self.current_audio.split('/')[-1]  # For Unix/Linux/Mac
            # song = self.current_audio.split('\\')[-1]  # For Windows
            song_name = song.replace('.mp3', '')
            song_box.insert(END, song_name)
            self.audio_files.append(self.current_audio)  # Store the full path in the list

    def add_many_load_audio(self):
        """"
         Function to load multiple audio files
         cho phep nguoi dung tai nhieu file cung luc
        """
        current_audios = filedialog.askopenfilenames(title='Choose songs', filetypes=(('MP3 Files', '*.mp3'),))
        for song in current_audios:
            song_name = song.split('/')[-1].replace('.mp3', '')  # For Unix/Linux/Mac
            # song_name = song.split('\\')[-1].replace('.mp3', '')  # For Windows
            song_box.insert(END, song_name)
            self.audio_files.append(song)  # Store the full path in the list

    def start_audio(self):
        """"
        Function to start playing the selected audio file
        """
        selected_index = song_box.curselection()  # Get the index of the selected song
        if selected_index:  # Ensure an item is selected
            current_audio_path = self.audio_files[selected_index[0]]  # Get the full path from the list
            try:
                pygame.mixer.music.load(current_audio_path)  # Load the selected song
                pygame.mixer.music.play(loops=0)  # Play the song
                print(f"Now playing: {song_box.get(selected_index)}")
                self.paused = False  # Ensure paused is False when the song starts playing
            except Exception as e:
                print(f"Error playing {current_audio_path}: {e}")

    def pause_audio(self):
        """"
        Function to pause and unpause the music
        """
        if self.paused:
            pygame.mixer.music.unpause()  # Resume the song
            self.paused = False
            pause_button.config(text="Pause")
        else:
            pygame.mixer.music.pause()  # Pause the song
            self.paused = True
            pause_button.config(text="Resume")

    def mute_unmute(self):
        """"
        Function to turn on or off the volume
        """
        if pygame.mixer.music.get_volume() > 0:
            self.last_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            mute_button.config(text="Unmute")
        else:
            pygame.mixer.music.set_volume(self.last_volume)
            mute_button.config(text="Mute")

    def set_volume(self, volume):
        """"
        Function to set the volume
        """
        pygame.mixer.music.set_volume(float(volume) / 100)
# Ham main test thoi
if __name__ == '__main__':
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

    # Add commands to the menu
    add_song_menu.add_command(label="Add One Song To Playlist", command=audio_engine.one_load_audio)
    add_song_menu.add_command(label="Add Many Songs To Playlist", command=audio_engine.add_many_load_audio)

    # Create a control frame for buttons
    control_frame = Frame(root)
    control_frame.pack(pady=20)

    # Create buttons to start and pause the song
    play_button = Button(control_frame, text="Play Song", command=audio_engine.start_audio)
    play_button.grid(row=0, column=0, padx=10)

    # Create a pause/resume button
    pause_button = Button(control_frame, text="Pause", command=audio_engine.pause_audio)
    pause_button.grid(row=0, column=1, padx=10)

    # Create a Mute/Unmute buton
    mute_button = Button(control_frame, text="Mute", command=audio_engine.mute_unmute)
    mute_button.grid(row=0, column=7, padx=5)

    # Create a volume control scale
    volume_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=audio_engine.set_volume, label="Volume")
    volume_slider.set(50)  # Set initial volume to 50%
    volume_slider.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()
