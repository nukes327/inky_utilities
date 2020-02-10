from inky import InkyPHAT
from PIL import Image

inky_display = InkyPHAT("yellow")
inky_display.set_border(inky_display.BLACK)

img = Image.open("test-screen.png")
inky_display.set_image(img)
inky_display.show()
