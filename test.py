import tkinter as tk
from PIL import ImageTk, Image, ImageGrab



root = tk.Tk()
root.geometry("3508x2480")

card = "cards/+/DigiScore_+_Design_Live Manipulation.png"

img = ImageTk.PhotoImage(Image.open(card))
this_label = tk.Label(root,
                        image=img,
                        width=750,
                        height=1050,
                        highlightthickness=0,
                        )
this_label.place(x=0, y=0)

root.mainloop()
