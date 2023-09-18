import pixie

image = pixie.Image(3500, 2480)
# image.fill(pixie.Color(128, 128, 128, 1))


img = pixie.read_image("cards/+/DigiScore_+_Content_AI Agent.png")

image.draw(
    img,
    pixie.translate(100, 100) *
    pixie.scale(0.2, 0.2) *
    pixie.translate(-450, -450)
)

#
# font = pixie.read_font("Ubuntu-Regular_1.ttf")
# # font = pixie.Font("Arial")
# font.size = 20
#
# text = "Typesetting is the arrangement and composition of text in graphic design and publishing in both digital and traditional medias."
#
# image.fill_text(
#     font,
#     text,
#     bounds = pixie.Vector2(180, 180),
#     transform = pixie.translate(10, 10)
# )




#
# ctx = image.new_context()
# ctx.paint = pixie.Paint(pixie.SOLID_PAINT)
# ctx.paint.color = pixie.Color(1, 0, 0, 1)
#
#
# ctx.fill_style = ctx.paint
# ctx.fill_text(0, 0, "hello world")
#
# ctx.fill_rect(50, 50, 100, 100)


image.write_file("text.png")