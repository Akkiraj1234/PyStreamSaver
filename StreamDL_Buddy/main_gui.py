from tkinter import Label
from tkinter import Tk


#rufe_dir()
info_dir={
    "window_size":"400x400",
    "backgroumd_color":"black",
    "text_color":"white"
}

#info_gathering
window_size=info_dir["window_size"]
background_color=info_dir["backgroumd_color"]
text_color=info_dir["text_color"]

# window()

window=Tk()
window.geometry(window_size)
window.config(background=background_color)


#lable
lable1=Label(
    window,
    text="will work on gui downloader",
    fg=text_color,
    bg=background_color
)
lable1.pack()

window.mainloop()