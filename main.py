import tkinter as tk
from tkinter import ttk
import urllib.request
import io
from PIL import ImageTk, Image, ImageGrab

import tkcap


# Master params
# master_page_size = (1000, 1500)  # A4 portrait
# master_page_rows = 2
# master_page_columns = 4

card_size_width = 750
card_size_depth = 1050

mode_list = [("Interface", "palegreen", "https://live.staticflickr.com/5533/9232097827_6b77e7d106_k_d.jpg"),
                 ("Design", "sienna1", "https://live.staticflickr.com/4044/4424964267_14c5a6f900_k_d.jpg"),
                 ("Goal", "silver", "https://live.staticflickr.com/4132/5048307585_51df161d35_k_d.jpg"),
                 ("Content", "gold1", "https://live.staticflickr.com/1946/43729984740_7159cfa87c_k_d.jpg"),
                 ("Language", "mediumorchid", "https://live.staticflickr.com/5052/5481137306_e138dca767_k_d.jpg"),
                 ("Feedback", "red1", "https://live.staticflickr.com/3049/3101950593_16e0528bd0_k_d.jpg"),
                 ("Flow", "royalblue1", "https://live.staticflickr.com/5052/5481137306_e138dca767_k_d.jpg")
                      ]

type_dict = {"+": {"name": "Opportunity",
                       "bg_for_expl": "white",
                       "text_col_for_explain": "black"
                       },
                 "-": {"name": "Challenge",
                       "bg_for_expl": "black",
                       "text_col_for_explain": "white"
                       },
                 "?": {"name": "Question",
                       "bg_for_expl": "gray70",
                       "text_col_for_explain": "black"
                       }
                 }

border = 25
image_size = (600, 400)

# def create_frame(container):
#     frame = tk.Frame(container)
#

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        img = image.resize(image_size)
        self.image = ImageTk.PhotoImage(img)

    def get(self):
        return self.image


class UI:
    def __init__(self):
        # set up canvas for card
        self.root = tk.Tk()
        # card_main_root.title('Replace')

        self.root.geometry("750x1050")  # card_size_width,
        #     card_size_depth)
        # )
        self.root.overrideredirect(True)

    def capture_screen_shot(self):
        # cap = tkcap.CAP(self.root)
        # cap.capture('test.png', overwrite=True)

        print(self.root.geometry())
        self.root.update()
        img = ImageGrab.grab(bbox=(46, 55, (750+46), (997+55)),
                             include_layered_windows=False,
                             all_screens=True
                             )
        img.save('test.png')


    def create_main_window(self):

        # todo - main card loop here
        # this_card_details = ["?",
        #              5,
        #              "Main Mechanics",
        #              "What are the most important score mechanics?",
        #              "CC BY-NC-ND 2.0",
        #              "https://live.staticflickr.com/1343/1098261686_f7aab03543_k_d.jpg",
        #              "Daniel Gasienica"
        #              ]

        this_card_details = ["+",
                             5,
                             "Codes",
                             "What do you want the musicians to do? What notation supports this?",
                             "CC BY-SA 2.0",
                             "https://live.staticflickr.com/139/327122302_c1414d8133_k_d.jpg",
                             "Alexander Henning Drach"]

        # this_card_details = ["-",
        #                      1,
        #                      "Poetics",
        #                      "Can you describe the poetic imagery of the score?",
        #                      "CC BY 2.0",
        #                      "https://live.staticflickr.com/7240/26263282734_a12f6a00cd_k_d.jpg",
        #                      "Derek Ewkpatnc Finch"
        #                      ]

        # general card params
        card_params_for_type = type_dict.get(this_card_details[0])
        card_type_name = card_params_for_type.get("name")
        card_bg_for_expl = card_params_for_type.get("bg_for_expl")
        card_col_for_text = card_params_for_type.get("text_col_for_explain")

        # outer params
        main_bg_colour = mode_list[this_card_details[1] - 1][1]
        type_symbol = this_card_details[0]
        bottom_id_text = f"{mode_list[this_card_details[1] - 1][0]} {card_type_name}"

        # inner params
        card_title = this_card_details[2]
        card_text = this_card_details[3]
        image_credit = this_card_details[6]
        images_cr = this_card_details[4]

        # get image
        try:
            url = this_card_details[5]
        except:
            url = mode_list[this_card_details[1] - 1][2]

        img = WebImage(url).get()

        # make background
        self.root.configure(background=main_bg_colour)

        # make canvas for image and triangle
        image_canvas = tk.Canvas(self.root, width=image_size[0], height=image_size[1], bg=main_bg_colour, highlightthickness=0)
        image_canvas.place(x=75, y=75)
        image_canvas.create_image(0, 0, anchor="nw", image=img) #, border=0)

        # add masking triangle
        tri_points = [-1, -1, 100, -1, -1, 100]
        image_canvas.create_polygon(tri_points, fill=main_bg_colour)

        # add credits
        image_canvas.create_text(20, image_size[1] - 20,
                                 font=('Helvetica 15'),
                                 anchor="w",
                                 text=f"{image_credit} ({images_cr})",
                                 fill="white"
                                 )

        # add symbol and type
        top_id_frame_text = tk.Label(self.root,
                                     text=type_symbol,
                                     font=('Helvetica 120 bold'),
                                     # justify="left",
                                     bg=main_bg_colour,
                                     foreground="white"
                                     )
        top_id_frame_text.place(x=20, y=5)

        # new canvas for text
        text_canvas = tk.Canvas(self.root, width=image_size[0], height=image_size[1] + 50, bg=card_bg_for_expl, highlightthickness=0)
        text_canvas.place(x=75, y=75+image_size[1])

        # add main title
        card_title = tk.Label(text_canvas,
                                 text=card_title,
                                 font=('Helvetica 60 bold'),
                                 justify="right",
                                 bg=card_bg_for_expl,
                                 foreground=card_col_for_text
                                 )
        card_title.place(x=20, y=10)

        # add main text
        main_text = tk.Label(text_canvas,
                             text=card_text,
                             font=('Helvetica 52'),
                             justify="left",
                             bg=card_bg_for_expl,
                             foreground=card_col_for_text,
                             wraplength=image_size[0]
                             )
        main_text.place(x=20, y=100)

        # bottom card type
        bottom_card_type = tk.Label(text_canvas,
                                     text=f">>>  {bottom_id_text}",
                                     font=('Helvetica 35 bold'),
                                     anchor="e",
                                     bg=card_bg_for_expl,
                                     foreground=card_col_for_text
                                     )
        bottom_card_type.place(x=20, y=380)


        # export as jpg here
        # todo - delete assets?
        # LOOP END

        self.root.after(100, self.capture_screen_shot)

        self.root.mainloop()

    # todo - build master card sheets here


if __name__ == "__main__":
    ui = UI()
    ui.create_main_window()