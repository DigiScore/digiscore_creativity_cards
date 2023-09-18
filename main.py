import tkinter as tk
import pandas as pd
import urllib.request
import io
from PIL import ImageTk, Image, ImageGrab
from time import sleep
from glob import glob


# Master A4 params
master_page_width = 1580 # 3500
master_page_height = 950  # 2480
master_page_size = f"{master_page_width}x{master_page_height}"  # A4 LANDSCAPE in pixels
master_page_columns = 4
master_page_rows = 2

# master card params
card_size_width = 750
card_size_depth = 1050
border = 25
image_size = (600, 400)
symbols = ["+", "-", "?"]
pdf_card_size_w = int(master_page_width / master_page_columns)
pdf_card_size_h = int(master_page_height / master_page_rows)
pdf_image_size = (pdf_card_size_w, pdf_card_size_h)
print(pdf_card_size_w, pdf_card_size_h)

# card data params
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

excel_file = "DS_Game_Cards_Image_Record.csv"


class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        img = image.resize(image_size)
        self.image = ImageTk.PhotoImage(img)

    def get(self):
        return self.image


class Card:
    def __init__(self):
        # set up canvas for card
        self.root = tk.Tk()
        self.root.geometry("750x1050")
        self.root.overrideredirect(True)

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
                img = WebImage(url).get()
            except:
                url = mode_list[this_card_details[2] - 1][2]
                img = WebImage(url).get()

            # make background
            self.root.configure(background=main_bg_colour)

            # make canvas for image and triangle
            image_canvas = tk.Canvas(self.root,
                                     width=image_size[0],
                                     height=image_size[1],
                                     bg=main_bg_colour,
                                     highlightthickness=0
                                     )
            image_canvas.place(x=75, y=75)
            image_canvas.create_image(0, 0,
                                      anchor="nw",
                                      image=img
                                      )

            # add masking triangle
            tri_points = [-1, -1, 100, -1, -1, 100]
            image_canvas.create_polygon(tri_points, fill=main_bg_colour)

            # add credits
            image_canvas.create_text(20, image_size[1] - 20,
                                     font=('Helvetica 15'),
                                     anchor="w",
                                     text=f"{image_credit} ({images_cr})",
                                     fill=main_bg_colour
                                     )

            # add symbol and type
            top_id_frame_text = tk.Label(self.root,
                                         text=self.type_symbol,
                                         font=('Helvetica 120 bold'),
                                         # justify="left",
                                         bg=main_bg_colour,
                                         foreground="white"
                                         )
            top_id_frame_text.place(x=20, y=5)

            # new canvas for text
            text_canvas = tk.Canvas(self.root,
                                    width=image_size[0],
                                    height=image_size[1] + 50,
                                    bg=card_bg_for_expl,
                                    highlightthickness=0
                                    )
            text_canvas.place(x=75, y=75+image_size[1])

            # add main title
            card_title = tk.Label(text_canvas,
                                  text=self.card_title,
                                  font=('Helvetica 50 bold'),
                                  justify="right",
                                  bg=card_bg_for_expl,
                                  foreground=card_col_for_text,
                                  wraplength=image_size[0] - 20
                                  )
            card_title.place(x=20, y=10)

            # add main text
            main_text = tk.Label(text_canvas,
                                 text=card_text,
                                 font=('Helvetica 50'),
                                 justify="left",
                                 bg=card_bg_for_expl,
                                 foreground=card_col_for_text,
                                 wraplength=image_size[0] - 20
                                 )
            main_text.place(x=20, y=120)

            # bottom card type
            bottom_card_type = tk.Label(text_canvas,
                                         text=f">>>  {bottom_id_text}",
                                         font=('Helvetica 35 bold'),
                                         anchor="e",
                                         bg=card_bg_for_expl,
                                         foreground=card_col_for_text
                                         )
            bottom_card_type.place(x=20, y=380)

            self.root.after(50, self.capture_screen_shot)

            self.root.update()

    def close_window(self):
        self.root.destroy()

    def make_backs(self):
        self.root.configure(background="white")

        # add DigiScore text
        ds_name = tk.Label(self.root,
                           text="The Digital Score",
                           font=('Helvetica 50 bold'),
                           bg="white",
                           foreground="gray70"
                           )
        ds_name.place(x=160, y=20)

        cards_name = tk.Label(self.root,
                           text="Creativity Cards",
                           font=('Helvetica 50 bold'),
                           bg="white",
                           foreground="gray70"
                           )
        cards_name.place(x=170, y=80)

        ds_url = tk.Label(self.root,
                           text="https://digiscore.github.io/",
                           font=('Helvetica 50 bold'),
                           bg="white",
                           foreground="gray70"
                           )
        ds_url.place(x=70, y=750)

        for sym in symbols:
            card_sym = tk.Label(self.root,
                           text=sym,
                           font=('Helvetica 400 bold'),
                           bg="white",
                           foreground="gray70"
                           )
            card_sym.place(x=260, y=230)

            img = ImageGrab.grab(bbox=(46, 55, (750 + 46), (997 + 55)),
                                 include_layered_windows=False,
                                 all_screens=True
                                 )
            img.save(f"cards/backs/DigiScore_{sym}_back_image.png")

            sleep(0.05)
            self.close_window()


        # self.root.after(50, self.capture_screen_shot)
        self.root.mainloop()

class PDF:
    def __init__(self):
        # set up canvas for card
        self.root = tk.Tk()
        self.root.geometry(master_page_size)
        self.root.overrideredirect(True)

    def process_list_of_cards(self, full_card_list):
        return [full_card_list[i:i + 8] for i in range(0, len(full_card_list), 8)]

    def pdf_build(self):
        # set pdf grid vars
        c = 0  # column
        r = 0  # row

        # iterate through each symbol

        for sym in symbols:
            # get the full list of paths for cards in this folder
            path = glob(f"cards/{sym}/*")

            # break that list into chunks of 8
            list_of_card_list = self.process_list_of_cards(path)

            list_of_image_objects = []
            list_of_empty_canvas = []

            # go through each chunk of 8 and build a PDF sheet
            for sheet, card_list in enumerate(list_of_card_list):
                # make a list of Image objects
                for card in card_list:
                    try:
                        img = Image.open(card)
                    except:
                        continue
                    resized_img = img.resize(pdf_image_size)
                    img_object = ImageTk.PhotoImage(resized_img)
                    list_of_image_objects.append(img_object)

                    # make a list of Labels
                    blank_canvas = tk.Canvas(self.root,
                                          width=pdf_card_size_w,
                                          height=pdf_card_size_h,
                                          highlightthickness=0,
                                          )
                    list_of_empty_canvas.append(blank_canvas)

                # place zipped lists onto root
                for i, img in enumerate(list_of_image_objects):
                    list_of_empty_canvas[i].place(x=c * pdf_card_size_w,
                                                  y=r * pdf_card_size_h)
                    list_of_empty_canvas[i].create_image(0, 0,
                                                         anchor="nw",
                                                         image=img)

                    c += 1
                    if c >= master_page_columns:
                        r += 1
                        c = 0

                    if r >= master_page_rows:
                        break

                sleep(5)
                # take screenshot
                grab = ImageGrab.grab(bbox=(40, 50, master_page_width, master_page_height),
                                    include_layered_windows=False,
                                    all_screens=True
                                    )
                # safe_name = self.card_title.replace(" ", "_")
                # safe_name = safe_name.replace("/", "-")
                grab.save(f"cards/PDFs/DigiScore_{sym}_sheet_{sheet}.pdf")

        self.root.mainloop()


if __name__ == "__main__":
    # build = Card()
    # build.create_full_deck()
    # build.close_window()

    build_pdf = PDF()
    build_pdf.pdf_build()

    # backs = Card()
    # backs.make_backs()
