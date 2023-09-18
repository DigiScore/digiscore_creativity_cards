from processing_py import *
import pandas as pd
import urllib.request
import io
from PIL import ImageTk, Image, ImageGrab
from time import sleep
from glob import glob


# app = App(600,400) # create window: width, height
# app.background(0,0,0) # set background:  red, green, blue
# app.fill(255,255,0) # set color for objects: red, green, blue
# app.rect(100,100,200,100) # draw a rectangle: x0, y0, size_x, size_y
# app.fill(0,0,255) # set color for objects: red, green, blue
# app.ellipse(300,200,50,50) # draw a circle: center_x, center_y, size_x, size_y
# app.redraw() # refresh the window



# Master A4 params
master_page_width = 3508
master_page_height = 2480
master_page_size = f"{master_page_width}x{master_page_height}"  # A4 LANDSCAPE in pixels
master_page_columns = 4
master_page_rows = 2

# master card params
card_size_width = 750
card_size_depth = 1050
border = 25
image_size = (600, 400)
symbols = ["+", "-", "?"]

# card data params
mode_list = [("Interface", (152,251,152), "https://live.staticflickr.com/5533/9232097827_6b77e7d106_k_d.jpg"),
                 ("Design", (255,130,71), "https://live.staticflickr.com/4044/4424964267_14c5a6f900_k_d.jpg"),
                 ("Goal", (192,192,192), "https://live.staticflickr.com/4132/5048307585_51df161d35_k_d.jpg"),
                 ("Content", (255,215,0), "https://live.staticflickr.com/1946/43729984740_7159cfa87c_k_d.jpg"),
                 ("Language", (186,85,211), "https://live.staticflickr.com/5052/5481137306_e138dca767_k_d.jpg"),
                 ("Feedback", (255,0,0), "https://live.staticflickr.com/3049/3101950593_16e0528bd0_k_d.jpg"),
                 ("Flow", (72,118,255), "https://live.staticflickr.com/5052/5481137306_e138dca767_k_d.jpg")
                      ]

type_dict = {"+": {"name": "Opportunity",
                   "bg_for_expl": (255,255,255),
                   "text_col_for_explain": (0,0,0)
                   },
             "-": {"name": "Challenge",
                   "bg_for_expl": "black",
                   "text_col_for_explain": (255,255,255)
                   },
             "?": {"name": "Question",
                   "bg_for_expl": (179,179,179),
                   "text_col_for_explain": (0,0,0)
                   }
             }

excel_file = "DS_Game_Cards_Image_Record.csv"



class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.img = image.resize(image_size)
        # self.image = ImageTk.PhotoImage(img)

    def get(self):
        return self.img




class Card:
    def __init__(self):
        # set up canvas for card
        self.root = App(card_size_width, card_size_depth)


    def capture_screen_shot(self):
        # capture screenshot of card
        img = ImageGrab.grab(bbox=(46, 55, (750+46), (997+55)),
                             include_layered_windows=False,
                             all_screens=True
                             )
        safe_name = self.card_title.replace(" ", "_")
        safe_name = safe_name.replace("/", "-")
        img.save(f"cards/{self.type_symbol}/DigiScore_{self.type_symbol}_{self.mode}_{safe_name}.png")


    def get_excel_data(self):
        full_card_df = pd.read_csv(filepath_or_buffer=excel_file,
                                sep=','
                                )

        # remove unused fields
        full_card_df.pop("Unnamed: 7")
        full_card_df.pop("Unnamed: 8")
        full_card_df.pop("Unnamed: 9")
        full_card_df.pop("Unnamed: 10")
        full_card_df.pop("Unnamed: 11")

        return full_card_df



    def create_full_deck(self):
        # import excel doc and return as pandas df
        full_card_df = self.get_excel_data()

        for this_card_details in full_card_df.itertuples():
            # print(this_card_details)

            # general card params
            card_params_for_type = type_dict.get(this_card_details[1])
            card_type_name = card_params_for_type.get("name")
            card_bg_for_expl = card_params_for_type.get("bg_for_expl")
            card_col_for_text = card_params_for_type.get("text_col_for_explain")

            # outer params
            main_bg_colour = mode_list[this_card_details[2] - 1][1]
            self.type_symbol = this_card_details[1]
            bottom_id_text = f"{mode_list[this_card_details[2] - 1][0]} {card_type_name}"
            self.mode = mode_list[this_card_details[2] - 1][0]

            # inner params
            self.card_title = this_card_details[3]
            card_text = this_card_details[4]
            image_credit = this_card_details[7]
            images_cr = this_card_details[5]

            # get image
            url = this_card_details[6]

            if pd.isna(url):
                url = mode_list[this_card_details[2] - 1][2]
            try:
                img_file = WebImage(url).get()
            except:
                url = mode_list[this_card_details[2] - 1][2]
                img_file = WebImage(url).get()
            print(img_file)
            img = self.root.loadImage(img_file)

            # make background
            self.root.background(color(152,251,152))

            # make canvas for image and triangle
            self.root.image(img, 75, 75, image_size[0], image_size[1])
            self.root.fill(main_bg_colour)
            self.root.text(f"{image_credit} ({images_cr})", 20, image_size[1] - 20)

            # add masking triangle
            self.root.triangle(74, 74, 100, 74, 74, 100)

            #
            # # add credits
            # self.root.te
            #
            # image_canvas.create_text(20, image_size[1] - 20,
            #                          font=('Helvetica 15'),
            #                          anchor="w",
            #                          text=f"{image_credit} ({images_cr})",
            #                          fill=main_bg_colour
            #                          )
            #
            # # add symbol and type
            # top_id_frame_text = tk.Label(self.root,
            #                              text=self.type_symbol,
            #                              font=('Helvetica 120 bold'),
            #                              # justify="left",
            #                              bg=main_bg_colour,
            #                              foreground="white"
            #                              )
            # top_id_frame_text.place(x=20, y=5)
            #
            # # new canvas for text
            # text_canvas = tk.Canvas(self.root,
            #                         width=image_size[0],
            #                         height=image_size[1] + 50,
            #                         bg=card_bg_for_expl,
            #                         highlightthickness=0
            #                         )
            # text_canvas.place(x=75, y=75+image_size[1])
            #
            # # add main title
            # card_title = tk.Label(text_canvas,
            #                       text=self.card_title,
            #                       font=('Helvetica 50 bold'),
            #                       justify="right",
            #                       bg=card_bg_for_expl,
            #                       foreground=card_col_for_text,
            #                       wraplength=image_size[0] - 20
            #                       )
            # card_title.place(x=20, y=10)
            #
            # # add main text
            # main_text = tk.Label(text_canvas,
            #                      text=card_text,
            #                      font=('Helvetica 50'),
            #                      justify="left",
            #                      bg=card_bg_for_expl,
            #                      foreground=card_col_for_text,
            #                      wraplength=image_size[0] - 20
            #                      )
            # main_text.place(x=20, y=120)
            #
            # # bottom card type
            # bottom_card_type = tk.Label(text_canvas,
            #                              text=f">>>  {bottom_id_text}",
            #                              font=('Helvetica 35 bold'),
            #                              anchor="e",
            #                              bg=card_bg_for_expl,
            #                              foreground=card_col_for_text
            #                              )
            # bottom_card_type.place(x=20, y=380)
            #
            # self.root.after(50, self.capture_screen_shot)
            #
            # self.root.update()



if __name__ == "__main__":
    build = Card()
    build.create_full_deck()
    # build.close_window()