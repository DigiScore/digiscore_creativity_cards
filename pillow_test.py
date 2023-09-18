from PIL import ImageTk, Image, ImageGrab

# Master A4 params
master_page_width = 3500
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
pdf_card_size_w = int(master_page_width / master_page_columns)
pdf_card_size_h = int(master_page_height / master_page_rows)
pdf_image_size = (pdf_card_size_w, pdf_card_size_h)
print(pdf_card_size_w, pdf_card_size_h)


img_test = Image.open("cards/+/DigiScore_+_Content_AI Agent.png")
img_test.resize((pdf_card_size_w, pdf_card_size_h))

new_im = Image.new('RGB', (master_page_width, master_page_height))

for i in range(0, master_page_width, pdf_card_size_w):
    for j in range(0, master_page_height, pdf_card_size_h):
        #I change brightness of the images, just to emphasise they are unique copies.
        im=Image.eval(img_test,lambda x: x+(i+j)/30)
        #paste the image at location i,j:
        new_im.paste(img_test, (i,j))

new_im.show()

