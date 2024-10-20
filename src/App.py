import os
import signal
import sys
import customtkinter
import tkinter
import traceback
from tkinter import filedialog
from PIL import Image
import psutil
import threading
from __version__ import __version__ as version
from MusicPlayer import MusicPlayer


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
           "skip-forward": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward-light.png")),
                                                   light_image=Image.open(os.path.join("Assets", "Player", "player-skip-forward.png")),
                                                   size=(30, 30)),
           "skip-back": customtkinter.CTkImage(dark_image=Image.open(os.path.join("Assets", "Player", "player-skip-back-light.png")),
                                                light_image=Image.open(os.path.join("Assets", "Player", "player-skip-back.png")),
                                                size=(30, 30)),
           "import"    : customtkinter.CTkImage(dark_image=Image.open("./Assets/UIAssets/import-light.png"),   
                                                             light_image=Image.open("./Assets/UIAssets/import.png"),  
                                                                      size=(30,30)),
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
            command=lambda: print("Next"),
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
            command=lambda: print("Previous"),
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
