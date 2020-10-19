import json
import os
import random
import ConfigHandler
from PIL import Image, ImageDraw, ImageFont


def welcome_plate(name, Config):
    folder = Config['welcome message']['template folder'] # 1600 700
    template_found = False
    while not template_found:
        template_file = str(folder + "/" + random.choice(os.listdir(folder)))
        if template_file.endswith(".png"):
            template_found = True

    image = Image.open(template_file)
    drawing = ImageDraw.Draw(image)
    font = ImageFont.truetype(Config["welcome message"]["font"],Config["welcome message"]["fontsize"])
    text_width, text_height = drawing.textsize(name.lower(), font)
    position = (int((1600 - text_width) / 2), int(((700 - text_height) / 2) - 37))
    drawing.text(position, name, tuple(Config["welcome message"]["colour"]), font=font)

    image.save(Config['welcome message']['final file'])
