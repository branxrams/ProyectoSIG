
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from textToSpech import run_tests_and_additional_code
import textToSpech

from audio_visual_animation import TalkingHeadAnimator, VideoAudioCombiner

import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x600")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    300.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    543.0,
    298.0,
    image=image_image_2
)

canvas.create_text(
    31.0,
    52.0,
    anchor="nw",
    text="Nombre de la aplicacion",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    167.0,
    308.0,
    image=image_image_5
)

# Define a function to handle clicks on the image
def on_image_click2(event):
    print("Image clicked!")
    image_path = "prueba1.png"
    audio_path = "output.mp3"
    output_path = "video_prueba.mp4"
    output_sound_path = "video_con_audio.mp4"

    animator = TalkingHeadAnimator(image_path, audio_path, output_path)
    animator.create_animation()

    output_sound_path = "video_con_audio.mp4"

    combiner = VideoAudioCombiner(output_path, audio_path)
    combiner.combine_audio_with_video(output_sound_path)

    for file_to_delete in ["output.mp3", "video_prueba.mp4"]:
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
        
        for file_name in os.listdir("."):
            if file_name.endswith(".mp3"):
                os.remove(file_name)

# Bind the click event to the image
canvas.tag_bind(image_5, '<Button-1>', on_image_click2)


image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    47.0,
    314.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    167.0,
    192.0,
    image=image_image_7
)

# Define a function to handle clicks on the image
def on_image_click(event):
    print("Image clicked!")
    canvas.itemconfig(image_9, state='normal')
    canvas.itemconfig(entry_bg_1, state='normal')
    canvas.itemconfig(image_10, state='normal')
    entry_1.place(x=496.0, y=146.0, width=228.0, height=244.0)

# Bind the click event to the image
canvas.tag_bind(image_7, '<Button-1>', on_image_click)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    47.0,
    194.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    493.0,
    268.0,
    image=image_image_9
)

canvas.itemconfig(image_9, state='hidden')

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    610.0,
    269.0,
    image=entry_image_1
)

canvas.itemconfig(entry_bg_1, state='hidden')

entry_1 = Text(
    bd=0,
    bg="#A2B041",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=496.0,
    y=146.0,
    width=228.0,
    height=244.0
)

entry_1.place_forget()

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    345.0,
    326.0,
    image=image_image_10
)
canvas.itemconfig(image_10, state='hidden')

# Define a function to handle clicks on the image
def on_image_click1(event):
    print("Image clicked!1")
    canvas.itemconfig(image_9, state='hidden')
    canvas.itemconfig(entry_bg_1, state='hidden')
    canvas.itemconfig(image_10, state='hidden')
    mensaje = entry_1.get("1.0", "end")
    textToSpech.mensaje1 = mensaje
    run_tests_and_additional_code()
    entry_1.place_forget()

# Bind the click event to the image
canvas.tag_bind(image_10, '<Button-1>', on_image_click1)

window.resizable(False, False)
window.mainloop()