from PIL import Image, ImageOps
import pyautogui
import math

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

img = Image.open(input("What is the filename of the file Include the file extension? "))
input("Please move your cursor to the top left edge of your drawing Plane: Press enter to contiue ")
topLeft = pyautogui.position()
input("Please move your cursor to the bottom right edge of your drawing Plane: Press enter to continue ")
bottomRight = pyautogui.position()
input("Please move your mouse to the dark side of the gray scale slider: Press enter to continue ")
sliderDark = pyautogui.position()
input("Please move your mouse to the light side of the gray scale slider: Press enter to continue ")
sliderLight = pyautogui.position()
scaleFactor = int(input("What scale factor do you want to use? Low = More resolution but longer drawing time "))


screenWidth, screenHeight = pyautogui.size()

grayScale = ImageOps.grayscale(img)

pix = grayScale.load()
print(pix[0,0])

xRange = math.floor(grayScale.width/scaleFactor)
yRange = math.floor(grayScale.height/scaleFactor)


xstep = (bottomRight[0] - topLeft[0]) / xRange
ystep = (bottomRight[1] - topLeft[1]) /yRange
lightStepX = (sliderDark[0] - sliderLight[0]) if (sliderDark[0] > sliderLight[0]) else (sliderLight[0] - sliderDark[0]) / 255
lightStepY = (sliderDark[1] - sliderLight[1]) if (sliderDark[0] > sliderLight[0]) else (sliderLight[0] - sliderDark[0]) / 255

print(2*"\n")
print("Running with the following stats")
print(f"xStep: {xstep}")
print(f"xRange: {xRange}")
print(f"yStep: {ystep}")
print(f"yRange {yRange}")
print(f"brightnessStep X: {lightStepX}")
print(f"brightnessStep Y: {lightStepY}")
DarkIsLeft = True if (sliderDark[0] < sliderLight[0]) else False
prev = -1
for x in range(xRange):
    for y in range(yRange):
        # Click the brightness
        brightness = pix[x*scaleFactor,y*scaleFactor]
        if brightness != prev:
            pyautogui.moveTo(sliderDark[0] + lightStepX*brightness if (DarkIsLeft) else sliderLight[0] + lightStepX*brightness,
                            sliderDark[1] if (DarkIsLeft) else sliderLight[1])
            pyautogui.click()
            prev = brightness
        

        # Click the pixel
        pyautogui.moveTo(topLeft[0] + xstep*x, topLeft[1] + ystep*y)
        pyautogui.click()