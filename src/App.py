import os
import signal
import sys
import customtkinter
import tkinter
import traceback
import webbrowser
import pygame
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
        """
        Initialize the App class
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

        self.imageCache = {
            # Add your images here
           "empty": customtkinter.CTkImage(Image.open(os.path.join("Assets", "UIAssets", "empty.png")), size=(1, 1)),
           "playing": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-pause-light.png")),
                                              light_image=Image.open(os.path.join("Assets", "Player", "player-pause.png")),
                                              size=(32, 32)),
           "paused": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-play-light.png")),
                                              light_image=Image.open(os.path.join("Assets", "Player", "player-play.png")),
                                              size=(32, 32)),
           "shuffle": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-shuffle-light.png")),
                                              light_image=Image.open(os.path.join("Assets", "Player", "player-shuffle.png")),
                                              size=(25, 25)),
           "loop": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "loop-light.png")),
                                               light_image=Image.open(os.path.join("Assets", "Player", "loop.png")),
                                               size=(25, 25)),
           "loop-off": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "loop-off-light.png")),
                                               light_image=Image.open(os.path.join("Assets", "Player", "loop-off.png")),
                                               size=(25, 25)),
           "loop-on": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "loop-off.png")),
                light_image=Image.open(os.path.join("Assets", "Player", "loop-off-light.png")),
                size=(25, 25)),

           "skip-forward": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward-light.png")),
                                                   light_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward.png")),
                                                   size=(30, 30)),
           "skip-back": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-back-light.png")),
                                                light_image=Image.open(os.path.join("Assets", "Player", "player-skip-back.png")),
                                                size=(30, 30)),
           "import"    : customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/import-light.png"),   
                                                             light_image=Image.open("./Assets/UIAssets/import.png"),  
                                                                      size=(30,30)),
            "github"       : customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/code-light.png"),      
                                                   light_image=Image.open("./Assets/UIAssets/code.png"),          
                                                                     size=(25,25)),
            "settings"     : customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/settings-light.png"),     
                                                          light_image=Image.open("./Assets/UIAssets/settings.png"),      
                                                                  size=(25,25)),
            "mute" : customtkinter.CTkImage(dark_image= Image.open("./Assets/UIAssets/mute-light.png"), 
                                            light_image= Image.open("./Assets/UIAssets/mute-black.png"), 
                                            size=(25,25)) , 
            "unmute" : customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/unmute-light.png"),  
                                              light_image=Image.open("./Assets/UIAssets/unmute-black.png"), 
                                              size=(25,25)) , 
        }
        self.loop = False
        self.mute = False
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
        self.west_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (175 / self.WIDTH), height=self.HEIGHT * (430 / self.HEIGHT), corner_radius=0)
        self.west_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), rowspan=4)
        
        self.north_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH), height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.north_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=(5, 0))

        self.center_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH), height=self.HEIGHT * (200 / self.HEIGHT), corner_radius=8)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.south_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (350 / self.WIDTH), height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.south_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=(0, 5))

        self.interface_frame = customtkinter.CTkFrame(master=self, width=self.WIDTH * (195 / self.WIDTH), height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
        self.interface_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=(5, 0))

        self.east_frame = customtkinter.CTkTabview(master=self, width=self.WIDTH * (195 / self.WIDTH), height=self.HEIGHT * (100 / self.HEIGHT), corner_radius=8)
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
            hover_color=self. interface_frame.cget("bg_color"), 
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

        self.listframe = customtkinter.CTkFrame(
            master=self.east_frame.tab("Imported"), 
            width=150,  
            height=175, 
            corner_radius=8
        )
        self.listframe.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER) 

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
            command=lambda: self.play_search(self.index_entry.get())
        )
        self.playbutton.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)
    #WEST FRAME
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

        #setting button
        self.settings_button = customtkinter.CTkButton(
            master=self.west_frame,
            font=(self.FONT, -12),
            text="",
            image=self.imageCache.get("settings"),
            bg_color='transparent',
            fg_color='transparent',
            hover_color=self.west_frame.cget("bg_color"),
            width=5,
            height=5,
            command= lambda : self.draw_settings_frame() ,
        )
        self.settings_button.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)
        #github link 
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
            command= lambda : self.muteEvent(),
        )
        self.mute_button.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)

     #SOUTH FRAME
        self.import_button = customtkinter.CTkButton(
            master = self.south_frame,
            command= lambda : self.import_files() ,
            image=self.imageCache.get("import"),
            fg_color='transparent',
            hover_color=self.south_frame.cget("bg_color"),
            text="Import Song(s)",
            font= (self.FONT, -14),
            width=240,
            height=50,
            text_color=self.logolabel.cget("text_color")
        )
        self.import_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

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
        for index, song in enumerate(self.music_player.get_all_tracks()):
            self.song_box.insert(tkinter.END, f"{index + 1}. {song}\n") 

    def shuffle(self):
        """
        Shuffle
        """
        self.music_player.shuffle_playlist()
        self.update_song_box()
        self.play_search("1")

    def loopEvent(self) ->None : 

        """
        Set the Loop state 
        """
        if self.loop == True : 
            self.loop = False
            self.loop_button.configure(state = "normal" , image = self.imageCache["loop"])
        else : 
            self.loop = True 
            self.loop_button.configure(state ="normal" , image = self.imageCache["loop-off"])
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
            self.music_player.play_at_index(int(index_label) - 1)
            self.playpause_button.configure(state="NORMAL", image=self.imageCache["playing"])
            self.next_button.configure(state="NORMAL")
            self.previous_button.configure(state="NORMAL")

        except Exception as e:
            print(traceback.format_exc())
        self.playbutton.configure(state=tkinter.NORMAL)

    def raise_above_all(self, window:customtkinter.CTkToplevel) -> None:
            """r
            Raises a window above all other window 
            Args:
                window (tkinter.Tk): The window to raise
            """
            window.attributes("-topmost", 1)
            window.attributes("-topmost", 0)
    def playpause(self) -> None:
        """
        Play or pause
        """
        if self.music_player.is_playing:
            self.music_player.pause()
            self.playpause_button.configure(state="normal", image=self.imageCache["paused"])
        else:
            self.music_player.play()
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
    def draw_settings_frame(self) -> None:
        """
        Draws the settings frame.
        """
        self.settings_window = customtkinter.CTkFrame(
            master=self, width=self.WIDTH * (755 / self.WIDTH), height=self.HEIGHT * (430 / self.HEIGHT), corner_radius=0
        )
        self.settings_window.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.settings_frame = customtkinter.CTkFrame(
            master=self.settings_window, width=350, height=380, corner_radius=10
        )
        self.settings_frame.place(relx=0.25, rely=0.47, anchor=tkinter.CENTER)

        self.setting_header = customtkinter.CTkLabel(
            master=self.settings_frame, text="Settings", font=(self.FONT, -18)
        )
        self.setting_header.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.general_frame = customtkinter.CTkTabview(master=self.settings_frame, width=300, height=160)
        self.general_frame.place(relx=0.5, rely=0.34, anchor=tkinter.CENTER)

        self.general_frame.add("General")
        self.general_header = customtkinter.CTkLabel(
            master=self.general_frame.tab("General"), text="General", font=(self.FONT, -16)
        )
        self.general_header.place(relx=0.2, rely=0.15, anchor=tkinter.CENTER)

        self.autoplay_box = customtkinter.CTkSwitch(
            master=self.general_frame.tab("General"),
            text="Autoplay",
            font=(self.FONT, -12),
            command=lambda:autoplay_event(),
            width=50,
        )
        self.autoplay_box.place(relx=0.28, rely=0.4, anchor=tkinter.CENTER)
        if self.getSetting('autoplay') == 'true':
            self.autoplay_box.select()
        
        def autoplay_event() ->None :
           pass
if __name__ == "__main__":
    app = App()
    app.mainloop()
