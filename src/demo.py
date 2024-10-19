import customtkinter
import tkinter

class MP3Player:
    def __init__(self, root):
        self.FONT = "Arial"
        self.settings = {"speed": 1.0}

        # Create a frame for effects
        self.effects_frame = customtkinter.CTkFrame(master=root, width=300, height=150)
        self.effects_frame.pack(pady=20, padx=20)

        # Create "Speed" label
        self.speed_header = customtkinter.CTkLabel(
            master=self.effects_frame, text="Speed", font=(self.FONT, -14)
        )
        # Adjust label position
        self.speed_header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        # Create speed adjustment slider
        self.speed_slider = customtkinter.CTkSlider(
            master=self.effects_frame,
            from_=0.25,
            to=1.75,
            number_of_steps=6,  # Set to 0 for continuous sliding
            width=165,
            height=10,
            command=self.setEffect
        )
        # Set default value and adjust slider position
        self.speed_slider.set(float(self.settings.get("speed")))
        self.speed_slider.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        # Create small labels to display speed values
        speeds = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
        slider_width = 165  # Width of the slider
        num_labels = len(speeds)

        for i, value in enumerate(speeds):
            # Calculate the relative x position for each label
            relx_position = (i / (num_labels - 1)) * slider_width / 300  # Normalize to frame width
            speed_label = customtkinter.CTkLabel(
                master=self.effects_frame, text=str(value), font=(self.FONT, -10), state=tkinter.DISABLED
            )
            speed_label.place(relx=relx_position + 0.5, rely=0.45, anchor=tkinter.CENTER)

    def setEffect(self, value):
        print(f"Tốc độ đã thay đổi: {value}")
        self.settings["speed"] = value

# Initialize main window
root = customtkinter.CTk()
app = MP3Player(root)
root.mainloop()
