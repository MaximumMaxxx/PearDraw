from DrawPD2 import findClosestColor, getColorFromImage
from PIL import Image


def test_findClosestColor():
    colors = [(0, 0, 0), (255, 255, 255),  (56, 74, 89), (100, 50, 70)]
    target = (0, 0, 1)
    assert findClosestColor(colors=colors, target=target) == (0, 0, 0)
    target = (243, 240, 255)
    assert findClosestColor(colors=colors, target=target) == (255, 255, 255)


def test_pixelFromImage():
    # Test loading an image and grabbing the color from it
    image = Image.open("Testimg.png")
    image = image.convert("RGB")
    x = 100
    y = 100
    color = getColorFromImage(x=x, y=y, image=image)  # Red
    assert color == (255, 0, 0)
    x = 700
    y = 200
    color = getColorFromImage(x=x, y=y, image=image)  # Green
    assert color == (0, 255, 0)
    x = 500
    y = 500
    color = getColorFromImage(x=x, y=y, image=image)  # Blue
    assert color == (0, 0, 255)
    x = 300
    y = 300
    color = getColorFromImage(x=x, y=y, image=image)  # White
    assert color == (255, 255, 255)
