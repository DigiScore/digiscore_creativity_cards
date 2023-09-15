import tkinter as tk


master_page_size = (210, 297) # A4 portrait
master_page_rows = 4
master_page_columns = 2

card_size_width = master_page_size[0] / master_page_columns
card_size_depth = master_page_size[1] / master_page_rows

bg_colour_list = ["palegreen",
                  "sienna1",
                  "silver",
                  "gold1",
                  "mediumorchid",
                  "red1",
                  "royalblue1"
                  ]

type_dict = {"+": {"name": "Opportunity",
                   "bg_for_expl": "white",
                   "text_c_for_explain": "black"
                   },
             "-": {"name": "Challenge",
                   "bg_for_expl": "black",
                   "text_c_for_explain": "white"
                   },
             "?": {"name": "Question",
                   "bg_for_expl": "gray30",
                   "text_c_for_explain": "white"
                   }
             }

test_card = ["?",
             3,
             "Main Mechanics",
             "What are the most important score mechanics?",
             "CC BY-NC-ND 2.0",
             "https://live.staticflickr.com/1343/1098261686_f7aab03543_k_d.jpg",
             "Daniel Gasienica"
             ]

border = 20
card_size_inner_w = int((card_size_width - border) / 2)
card_size_inner_d = int((card_size_depth - border) / 2)


# set up canvas for card
card_main = tk.Tk()

# todo - main card loop here

bg_colour = bg_colour_list[test_card[1] - 1]
card_canvas = tk.Canvas(card_main,
                        bg=bg_colour,
                        height=master_page_size[1],
                        width=master_page_size[0])

type_symbol = card_canvas.create_text(border, border,
                                      text=test_card[0],
                                      fill="black",
                                      font=('Helvetica 25 bold')
                                      )

type_text = card_canvas.create_text(border, card_size_inner_d,
                                    text=test_card[0],
                                    fill="black",
                                    font=('Helvetica 25 bold')
                                    )

card_title = tk.Text(card_canvas,
                     width=card_size_inner_w,
                     height=card_size_inner_d,
                     bg="red"
                     )

card_canvas.pack()

# text = tk.Text(canvas, width=120, height=40)
card_canvas.create_window((0, 0), window=card_title, anchor='nw')
card_title.insert('end', 'Hello World')

    # card_canvas.create_text(20, 145,
    #                                  text=test_card[3],
    #                                  fill="black",
    #                                  font=('Helvetica 25 bold')
    #                                  )
    #

# export as jpg here
# todo - delete assets?
# LOOP END
card_main.mainloop()

# todo - build master card sheets here