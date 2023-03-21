from PIL import Image

def change_background():
    img = Image.open("role/static/saved/role.png")
    new_background = Image.new("RGBA", img.size, (255, 255, 255))
    new_img = Image.alpha_composite(new_background, img)
    new_img.save("role/static/saved/role.png")
