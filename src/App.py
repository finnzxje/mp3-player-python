import os
import signal
import sys
import customtkinter
import tkinter
import traceback
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import psutil
from __version__ import __version__ as version
from MusicPlayer import MusicPlayer
from AudioEngine import AudioEngine

os.chdir(os.path.dirname(os.path.abspath(__file__)))
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme(os.path.join("Assets", "Themes", "MP3_MTH.json"))


class App(customtkinter.CTk):
    """
    The main MP3 application
    """

    def __init__(self) -> None:
        """        Initialize the App class
        """

        self.music_player = MusicPlayer()

        super().__init__()
        # Configure window
        self.title("MP3_PLAYER")
        self.iconbitmap(r".\Assets\UIAssets\mp3-player-icon_.ico")  # Icon for app
        self.WIDTH = 755
        self.HEIGHT = 430
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.maxsize(755, 430)
        self.found = False
        self.index_search = None
        self.mute = False
        self.autoplay = False
        self.remove_track = None
        self.found_remove = False

        self.imageCache = {
            # Add your images here
            "empty": customtkinter.CTkImage(Image.open(os.path.join("Assets", "UIAssets", "empty.png")), size=(1, 1)),
            "playing": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "player-pause-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "player-pause.png")),
                size=(32, 32)),
            "paused": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "player-play-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "player-play.png")),
                size=(32, 32)),
            "shuffle": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "player-shuffle-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "player-shuffle.png")),
                size=(25, 25)),
            "loop": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "loop-light.png")),
                                           light_image=Image.open(os.path.join("Assets", "Player", "loop.png")),
                                           size=(25, 25)),
            "loop-off": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "loop-off-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "loop-off.png")),
                size=(25, 25)),
            "loop-on": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "loop-off.png")),
                                              light_image=Image.open(
                                                  os.path.join("Assets", "Player", "loop-off-light.png")),
                                              size=(25, 25)),

            "skip-forward": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward.png")),
                size=(30, 30)),
            "skip-back": customtkinter.CTkImage(
                dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-back-light.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "player-skip-back.png")),
                size=(30, 30)),
            "import": customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/import-light.png"),
                                             light_image=Image.open("./Assets/UIAssets/import.png"),
                                             size=(30, 30)),
            "github": customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/code-light.png"),
                                             light_image=Image.open("./Assets/UIAssets/code.png"),
                                             size=(25, 25)),
            "settings": customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/settings-light.png"),
                                               light_image=Image.open("./Assets/UIAssets/settings.png"),
                                               size=(25, 25)),
            "mute": customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/mute-light.png"),
                                           light_image=Image.open("./Assets/UIAssets/mute-black.png"),
                                           size=(25, 25)),
            "unmute": customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/unmute-light.png"),
                                             light_image=Image.open("./Assets/UIAssets/unmute-black.png"),
                                             size=(25, 25)),
            "volume-muted": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume1.png")),
                size=(250, 100)
            ),
            "volume-muteda": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume1a.png")),
                size=(250, 100)
            ),
            "volume-low": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume2.png")),
                size=(250, 100)
            ),
            "volume-lowa": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume2a.png")),
                size=(250, 100)
            ),
            "volume-medium": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume3.png")),
                size=(250, 100)
            ),
            "volume-mediuma": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume3a.png")),
                size=(250, 100)
            ),
            "volume-high": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume4.png")),
                size=(250, 100)
            ),
            "volume-higha": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume4a.png")),
                size=(250, 100)
            ),
            "vol10": customtkinter.CTkImage(
                Image.open(os.path.join("Assets", "Player", "volume0.png")),
                size=(250, 100)
            ),
        }
        self.loop = False
        self.autoplay = True
        self.FONT = "Roboto Medium"

        self.createWidgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Free memory when closing

    def on_closing(self):
        """Terminate child processes"""
        self.destroy()
        self.quit()

        current_pid = psutil.Process().pid
        process = psutil.Process(current_pid)
        children = process.children(recursive=True)
        print(f"Terminating {len(children)} child processes.")
        for child in children:
            child.terminate()

        print("MP3 closed.")
        os.kill(current_pid, signal.SIGTERM)
        sys.exit()

    def createWidgets(self) -> None:
        """
        Create widget window
        """
        # Create frames
        self.west_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (175 / self.WIDTH),
                                                 height=self.HEIGHT * (430 / self.HEIGHT), corner_radius=0)
        self.west_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), rowspan=4)

        self.north_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH),
                                                  height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.north_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=(5, 0))

        self.center_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH),
                                                   height=self.HEIGHT * (200 / self.HEIGHT), corner_radius=8)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.south_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH),
                                                  height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.south_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=(0, 5))

        self.interface_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (195 / self.WIDTH),
                                                      height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.interface_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=(5, 0))

        self.east_frame = customtkinter.CTkTabview(master=self, width=self.WIDTH * (195 / self.WIDTH),
                                                   height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.east_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 0), pady=(0, 5), rowspan=3)
        self.east_frame.add("Imported")
        self.east_frame.add("Export")
        self.east_frame.tab("Imported").grid_columnconfigure(0, weight=1)
        self.east_frame.tab("Export").grid_columnconfigure(0, weight=1)

        # Buttons
        self.shuffle_button = customtkinter.CTkButton(
            master=self.interface_frame,
            image=self.imageCache.get("shuffle"),
            command=lambda: self.shuffle(),
            text="",
            width=5,
            height=5,
            fg_color='transparent',
            hover_color=self.interface_frame.cget("bg_color"),
            corner_radius=8
        )

        self.loop_button = customtkinter.CTkButton(
            master=self.interface_frame,
            image=self.imageCache.get("loop-off"),
            command=lambda: self.loopEvent(),
            text="",
            width=5,
            height=5,
            fg_color='transparent',
            hover_color=self.interface_frame.cget("bg_color"),
            corner_radius=8
        )

        self.next_button = customtkinter.CTkButton(
            master=self.interface_frame,
            image=self.imageCache.get("skip-forward"),
            command=lambda: self.next_song(),
            text="",
            width=5,
            height=5,
            fg_color='transparent',
            hover_color=self.interface_frame.cget("bg_color"),
            corner_radius=8,
            state=tkinter.DISABLED
        )

        self.previous_button = customtkinter.CTkButton(
            master=self.interface_frame,
            image=self.imageCache.get("skip-back"),
            command=lambda: self.previous_song(),
            text="",
            width=5,
            height=5,
            fg_color='transparent',
            hover_color=self.interface_frame.cget("bg_color"),
            corner_radius=8,
            state=tkinter.DISABLED
        )

        self.playpause_button = customtkinter.CTkButton(
            master=self.interface_frame,
            image=self.imageCache.get("paused"),
            command=lambda: self.playpause(),
            text="",
            width=5,
            height=5,
            fg_color='transparent',
            hover_color=self.interface_frame.cget("bg_color"),
            corner_radius=8,
            state=tkinter.DISABLED
        )

        # Place buttons
        self.shuffle_button.place(relx=0.16, rely=0.5, anchor=tkinter.CENTER)
        self.loop_button.place(relx=0.84, rely=0.5, anchor=tkinter.CENTER)
        self.previous_button.place(relx=0.33, rely=0.5, anchor=tkinter.CENTER)
        self.playpause_button.place(relx=0.50, rely=0.5, anchor=tkinter.CENTER)
        self.next_button.place(relx=0.67, rely=0.5, anchor=tkinter.CENTER)

        # Right (East) Frame
        self.search_entry = customtkinter.CTkEntry(
            master=self.east_frame.tab("Imported"),
            width=150,
            height=25,
            placeholder_text="Search for audio"
        )
        self.search_entry.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
        self.search_entry.bind("<Return>", lambda x: self.search_song())

        self.search_entry_remove = customtkinter.CTkEntry(
            master=self.east_frame.tab("Export"),
            width=150,
            height=25,
            placeholder_text="Search for audio"
        )
        self.search_entry_remove.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
        self.search_entry_remove.bind('<Return>', lambda event: self.search_song_remove())

        self.listframe = customtkinter.CTkFrame(
            master=self.east_frame.tab("Imported"),
            width=150,
            height=175,
            corner_radius=8
        )
        self.listframe.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.listframe_remove = customtkinter.CTkFrame(
            master= self.east_frame.tab("Export"),
            width=150,
            height=175,
            corner_radius=8
        )
        self.listframe_remove.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.song_box_remove = customtkinter.CTkTextbox(
            master=self.listframe_remove,
            width=140,
            height=175,
            bg_color='transparent',
            fg_color='transparent',
            corner_radius=8
        )
        self.song_box_remove.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.song_box = customtkinter.CTkTextbox(
            master=self.listframe,
            width=140,
            height=175,
            bg_color='transparent',
            fg_color='transparent',
            corner_radius=8
        )
        self.song_box.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.index_entry = customtkinter.CTkEntry(
            master=self.east_frame.tab("Imported"),
            width=150,
            height=25,
            placeholder_text="Enter index of audio"
        )
        self.index_entry.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

        self.playbutton = customtkinter.CTkButton(
            master=self.east_frame.tab("Imported"),
            text="Play",
            width=150,
            height=25,
            command=lambda: self.play_search_song()
        )
        self.playbutton.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

        # Create remove
        self.removebutton = customtkinter.CTkButton(
            master= self.east_frame.tab("Export"),
            text="Remove",
            width=150,
            height=25,
            command = lambda : self.delete_song()
        )
        self.removebutton.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)
        # WEST FRAME
        self.logolabel = customtkinter.CTkLabel(
            master=self.west_frame, text=f" MP3_PROMAX{version}", font=(self.FONT, -16)
        )
        self.logolabel.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

        self.themelabel = customtkinter.CTkLabel(master=self.west_frame, text="Appearance Mode:")
        self.themelabel.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.thememenu = customtkinter.CTkOptionMenu(
            master=self.west_frame,
            values=["System", "Dark", "Light"],
            command=lambda x: AudioEngine.change_theme(x)
        )
        self.thememenu.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # setting button
        self.autoplay_box = customtkinter.CTkSwitch(
            master=self.west_frame,
            command=self.toggle_autoplay, 
            text="", 
            width=50,
        )
        self.autoplay_box.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)

        if self.music_player.get_setting('autoplay') == 'true':
            self.autoplay_box.select()
        else:
            self.autoplay_box.deselect()


        # github link
        self.github_button = customtkinter.CTkButton(
            master=self.west_frame,
            font=(self.FONT, -12),
            text="",
            image=self.imageCache["github"],
            bg_color='transparent',
            fg_color='transparent',
            hover_color=self.west_frame.cget("bg_color"),
            width=5,
            height=5,
            command=lambda: webbrowser.open("https://github.com/finnzxje/mp3-player-python", new=2),
        )
        self.github_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.mute_button = customtkinter.CTkButton(
            master=self.west_frame,
            font=(self.FONT, -12),
            text="",
            image=self.imageCache.get("unmute"),
            bg_color='transparent',
            fg_color='transparent',
            hover_color=self.west_frame.cget("bg_color"),
            width=5,
            height=5,
            corner_radius=16,
            command=lambda: self.muteEvent(),
        )
        self.mute_button.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)

        # SOUTH FRAME
        self.import_button = customtkinter.CTkButton(
            master=self.south_frame,
            command=lambda: self.import_files(),
            image=self.imageCache.get("import"),
            fg_color='transparent',
            hover_color=self.south_frame.cget("bg_color"),
            text="Import Song(s)",
            font=(self.FONT, -14),
            width=240,
            height=50,
            text_color=self.logolabel.cget("text_color")
        )
        self.import_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # NORTH FRAME
        self.songlabel = customtkinter.CTkButton(
            master=self.north_frame,
            text=f"Play Something!",
            width=240,
            height=50,
            font=(self.FONT, -14),
            command=lambda: self.draw_lyrics_box(),
            fg_color='transparent',
            hover_color=self.north_frame.cget("bg_color"),
            text_color=self.logolabel.cget("text_color"),
            image=self.imageCache["empty"],
        )
        self.songlabel.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.progressbar = customtkinter.CTkSlider(master=self.north_frame, width=225, height=15, from_=0, to=100,
                                                   number_of_steps=100, command=lambda x: self.slider_event(x),
                                                   state=tkinter.DISABLED)
        self.progressbar.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.progressbar.set(0)
        self.progress_label_left = customtkinter.CTkLabel(
            master=self.north_frame, text="0:00", font=(self.FONT, -12), width=5
        )
        self.progress_label_left.place(relx=0.1, rely=0.7, anchor=tkinter.CENTER)

        self.progress_label_right = customtkinter.CTkLabel(
            master=self.north_frame, text="0:00", font=(self.FONT, -12), width=5
        )
        self.progress_label_right.place(relx=0.9, rely=0.7, anchor=tkinter.CENTER)

        # CREATE SONG VOLUME
        self.song_volume = customtkinter.CTkSlider(master=self.center_frame,
                                                   width=225, height=20, from_=0, to=100,
                                                   number_of_steps=100, command=lambda x: self.call_volume(x),
                                                   progress_color="#1DB954",
                                                   fg_color="#333333",
                                                   )
        self.song_volume.place(relx=0.57, rely=0.85, anchor=tkinter.CENTER)
        self.song_volume_left = customtkinter.CTkLabel(
            master=self.center_frame, text="Volume ", font=(self.FONT, -12), width=5
        )
        self.song_volume_left.place(relx=0.15, rely=0.85, anchor=tkinter.CENTER)

        self.song_volume_left_top = customtkinter.CTkLabel(
            master=self.center_frame, text="Min", font=(self.FONT, -12), width=5
        )
        self.song_volume_left_top.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.song_volume_right_top = customtkinter.CTkLabel(
            master=self.center_frame, text="Max", font=(self.FONT, -12), width=5
        )
        self.song_volume_right_top.place(relx=0.84, rely=0.7, anchor=tkinter.CENTER)

        # Now add the label to this frame
        self.volume_meter = customtkinter.CTkLabel(master=self.center_frame, text='', image=self.imageCache["volume-lowa"])
        self.volume_meter.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

    def delete_song(self):
        if self.found_remove == False:
            self.update_song_box()
        else :
            self.music_player.stop()

            self.music_player.remove_from_playlist(self.remove_track)
            self.music_player.remove_track()
            self.song_box_remove.delete("1.0", tkinter.END)
            self.song_box_remove.insert(tkinter.END, "The song has been successfully deleted.\n")
            self.song_box_remove.insert(tkinter.END, "Please delete the search bar and press enter to update again\n")
            self.reset_progress_bar()

    def play_search_song(self):
        """
        Check whether to run Search Audio or Enter Index
        """
        if self.found == True:
            self.found = False
            index = str(self.index_search + 1)
        else:
            index = str(self.index_entry.get())
        self.play_search(str(index))

    def search_song(self):
        """
       Search for songs in playlists. If the search keyword is empty, display the entire song list again.
        """
        self.found = False
        search_term = self.search_entry.get().strip().lower()
        self.song_box.delete("1.0", tkinter.END)

        if not search_term:
            self.update_song_box()
            return

        for index, song in enumerate(self.music_player.get_all_tracks()):
            if search_term in song.title.lower():
                self.index_search = index
                self.song_box.insert(tkinter.END, f"{index + 1}. {song.title}\n")
                self.found = True

        if not self.found:
            self.song_box.insert(tkinter.END, "No song found.\n")

    def search_song_remove(self):
        """
       Search for songs in playlists
        """
        self.found_remove = False
        search_term = self.search_entry_remove.get().strip().lower()

        if not search_term:
            self.update_song_box()
            return
        self.song_box_remove.delete("1.0", tkinter.END)

        for index, song in enumerate(self.music_player.get_all_tracks()):
            if search_term in song.title.lower():
                self.remove_track = song
                self.song_box_remove.insert(tkinter.END, f"{index + 1}. {song.title}\n")
                self.found_remove = True

        if not self.found_remove:
            self.song_box_remove.insert(tkinter.END, "No song found.\n")

    def reset_progress_bar(self):
        self.progressbar.configure(state=tkinter.DISABLED)
        self.progressbar.after_cancel(self.loop_reset_progressbar)
        self.progressbar.set(0)
        self.progress_label_right.configure(text=f"00:00")
        self.songlabel.configure(text=f"Play Something!")

        self.progress_label_left.configure(text=f"00:00")

    def call_volume(self, value ):
        """
        Call volume
        """
        self.music_player.set_volume(float(value) / 100)

        if value == 0:
            self.volume_meter.configure(image=self.imageCache.get("vol10"))
        elif 0 < value <= 12:
            self.volume_meter.configure(image=self.imageCache.get("volume-muted"))
        elif 12 < value <= 24:
            self.volume_meter.configure(image=self.imageCache.get("volume-muteda"))
        elif 24 < value <= 36:
            self.volume_meter.configure(image=self.imageCache.get("volume-low"))
        elif 36 < value <= 48:
            self.volume_meter.configure(image=self.imageCache.get("volume-lowa"))
        elif 48 < value <= 60:
            self.volume_meter.configure(image=self.imageCache.get("volume-medium"))
        elif 60 < value <= 82:
            self.volume_meter.configure(image=self.imageCache.get("volume-mediuma"))
        elif 82 < value <= 94:
            self.volume_meter.configure(image=self.imageCache.get("volume-high"))
        else :
            self.volume_meter.configure(image=self.imageCache.get("volume-higha"))

    def import_files(self):
        """
        Import file(s) from local machine
        """
        files_name = filedialog.askopenfilenames(title='Choose songs', filetypes=(('MP3 Files', '*.mp3'),))

        self.music_player.add_track_from_files(files_name)
        self.update_song_box()

    def update_song_box(self):
        """
        Update the song box
        :return:
        """
        self.song_box.delete("1.0", tkinter.END)
        self.song_box_remove.delete("1.0", tkinter.END)
        for index, song in enumerate(self.music_player.get_all_tracks()):
            self.song_box.insert(tkinter.END, f"{index + 1}. {song}\n")
            self.song_box_remove.insert(tkinter.END, f"{index + 1}. {song}\n")

    def shuffle(self):
        """
        Shuffle
        """
        self.music_player.shuffle_playlist()
        self.update_song_box()
        self.play_search("1")

    def loopEvent(self) -> None:

        """
        Set the Loop state
        """
        if self.loop == False:
            self.loop_button.configure(state="normal", image=self.imageCache["loop"])
            self.loop = True
            #self.music_player.on_loop()
        else:
            self.loop_button.configure(state="normal", image=self.imageCache["loop-off"])
            self.loop = False
            self.music_player.play()

    def muteEvent(self) -> None:
        """
             Set the mute button state
         """
        if self.mute:
            # if mute -> unmute
            self.mute = False
            self.mute_button.configure(state="normal", image=self.imageCache["unmute"])
        else:
            # if not mute -> mute
            self.mute = True
            self.mute_button.configure(state="normal", image=self.imageCache["mute"])
        self.music_player.mute()

    def play_search(self, index_label: str) -> None:
        """
        Play song in a box if user searches or chooses
        Args:
            index_label (str): The index of the song
        """
        self.playbutton.configure(state=tkinter.DISABLED)
        if index_label == "" or not index_label.isdigit():
            self.playbutton.configure(state=tkinter.NORMAL)
            return

        if int(index_label) > len(self.music_player.get_all_tracks()):
            self.playbutton.configure(state=tkinter.NORMAL)
            return
        try:
            self.songlabel.configure(text=self.music_player.get_all_tracks()[int(index_label) - 1].title)
            self.music_player.play_at_index(int(index_label) - 1)
            self.playpause_button.configure(state="NORMAL", image=self.imageCache["playing"])
            self.update_UI()

        except Exception as e:
            print(traceback.format_exc())
        self.playbutton.configure(state=tkinter.NORMAL)


    def playpause(self) -> None:
        """
        Play or pause
        """
        if self.music_player.is_playing:
            if self.music_player.is_ended():
                self.play_search(str(self.music_player.index + 1))
            else:
                self.music_player.pause()
                self.playpause_button.configure(state="normal", image=self.imageCache["paused"])
        else:
            self.music_player.pause()
            self.playpause_button.configure(state="normal", image=self.imageCache["playing"])

    def next_song(self):
        """
        Skip to the next song
        :return:
        """
        next_song_index = (self.music_player.index + 1) % len(self.music_player.playlist.tracks)
        self.play_search(str(next_song_index + 1))

    def previous_song(self):
        """
        Skip to the previous song
        :return:
        """
        previous_song_index = (self.music_player.index - 1) % len(self.music_player.playlist.tracks)
        self.play_search(str(previous_song_index + 1))

    def toggle_autoplay(self):
        """
        func change state of
        """
        if self.autoplay_box.get():
            messagebox.showinfo("MESSAGE", "Autoplay ON") #show message when on
        else:
            messagebox.showinfo("MESSAGE", "Autoplay OFF") #show message when off
  
        self.autoplay_event()
        state = "Bật" if self.autoplay_box.get() else "Tắt"
        # save state to setting ( config.json)
        self.music_player.save_setting('autoplay', 'true' if state == "Bật" else 'false')
        

    def slider_event(self, value):
        """
        Update the song according to the progress bar
        :return:
        """
        self.playpause_button.configure(state="NORMAL", image=self.imageCache["playing"])
        self.music_player.is_playing = True
        seconds = value / 100 * self.music_player.get_duration()
        self.music_player.seek(seconds)
        self.update_UI()

    def update_UI(self):
        """
        Update the UI
        :return:
        """
        self.next_button.configure(state="NORMAL")
        self.previous_button.configure(state="NORMAL")
        self.progressbar.configure(state=tkinter.NORMAL)
        self.progress_label_right.configure(
            text=f"{int(self.music_player.get_duration() / 60):02d}:{int(self.music_player.get_duration() % 60):02d}")
        self.update_progressbar()

    def update_progressbar(self):
        """
        Update the progress bar
        :return:
        """
        if self.music_player.is_ended():
            self.progressbar.set(100)
            self.progress_label_left.configure(
                text=f"{int(self.music_player.get_duration() / 60):02d}:{int(self.music_player.get_duration() % 60):02d}")
            self.handle_ending()

        else:
            curr_time = self.music_player.get_position() / 1000
            progress = curr_time / self.music_player.get_duration()
            self.progressbar.set(int(progress * 100))
            self.progress_label_left.configure(
                text=f"{int(curr_time / 60):02d}:{int(curr_time % 60):02d}")
            self.loop_reset_progressbar = self.progressbar.after(1000, self.update_progressbar)

    def autoplay_event(self) -> None:
        self.autoplay = not self.autoplay

    def draw_lyrics_box(self):
        pass

    def handle_ending(self):
        """
        Handles the ending of the music
        :return:
        """
        if self.loop:
            self.reset_progress_bar()
            self.play_search(str(self.music_player.index + 1))
        elif self.autoplay:
            self.play_search(str((self.music_player.index + 2) % len(self.music_player.playlist.tracks)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
