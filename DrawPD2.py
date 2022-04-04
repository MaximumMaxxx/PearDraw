from PIL import Image
import pyautogui
import math
import time
import json

pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = True

isleft = False

SCROLLTIMEOUT = 0.75  # The timeout to allow the scroll animation to complete


def getScreenBounds() -> tuple[tuple[int, int], tuple[int, int]]:
    input("Please move your cursor to the top left edge of your drawing Plane: Press enter to contiue ")
    topLeft = pyautogui.position()
    input("Please move your cursor to the bottom right edge of your drawing Plane: Press enter to continue ")
    bottomRight = pyautogui.position()
    return((topLeft, bottomRight))


def loadUsersImage():
    filename = input(
        "What is the name of the image file? (Include the file extension) ")
    img = Image.open(filename)
    rgb = img.convert("RGB")
    return rgb


def getColorsAndPositions(colors, side):
    print(f"Please scroll the color selector to the {side} side \n")
    iny = input(
        "Hover over one of the colors and press enter or 'n' then enter when you are done. ")
    if iny == "n":
        return colors
    x, y = pyautogui.position()
    # Didn't return out of the function
    im = pyautogui.screenshot()
    px = im.getpixel((x, y))
    colors.append((px, (x, y)))
    return getColorsAndPositions(colors=colors, side=side)


def colorDifference(base: tuple[int, int, int], target: tuple[int, int, int]):
    diff = 0
    for index, baseColor in enumerate(base):
        diff += abs(target[index]-baseColor)
    return(diff)


def findClosestColor(colors: list[tuple[int, int, int]], target: tuple[int, int, int]):
    bestDifference = 1000
    for color in colors:
        diff = colorDifference(color, target)
        if diff < bestDifference:
            bestColor = color
            bestDifference = diff
    return bestColor


def getCombinedColorsList(left, right):
    combined = []
    for combo in left:
        if combo[0] not in combined:
            combined.append(combo[0])
    for combo in right:
        if combo[0] not in combined:
            combined.append(combo[0])
    return(combined)


def getRanges(scalefactor, img: Image.Image):
    xrange = math.floor(img.width/scalefactor)
    yrange = math.floor(img.height/scalefactor)
    return((xrange, yrange))


def getButton(side: str):
    input(f"Please hover over the {side} button and press enter ")
    return pyautogui.position()


def findListColorIsIn(left: list[tuple[tuple[int, int, int], tuple[int, int, int]]], right: list[tuple[tuple[int, int, int], tuple[int, int, int]]], target: tuple[int, int, int]):
    # Index 0 is colors
    # Index 1 is position
    for item in left:
        if item[0] == target:
            return left, "L"
    return right, "R"


def getCoordsOfColor(list: list[tuple[tuple[int, int, int], tuple[int, int, int]]], color: tuple[int, int, int]):
    for item in list:
        if item[0] == color:  # If the color is the color
            return item[1]


def selectClosestColor(colors, target: tuple[int, int, int], leftcolors: list[tuple[tuple[int, int, int], tuple[int, int, int]]], rightcolors: list[tuple[tuple[int, int, int], tuple[int, int, int]]], rightPos: tuple[int, int], leftPos: tuple[int, int]):
    global isleft
    closest = findClosestColor(colors, target)
    print(f"{closest} is the closest color to {target}\n Also isleft is {isleft}")
    list, targetSide = findListColorIsIn(leftcolors, rightcolors, closest)

    if targetSide == "R":
        if isleft:
            rx, ry = rightPos

            # Scroll to the right
            pyautogui.moveTo(rx, ry)
            pyautogui.click()
            isleft = False
            time.sleep(SCROLLTIMEOUT)
        x, y = getCoordsOfColor(list=list, color=closest)
        pyautogui.moveTo(x, y)
        pyautogui.click()
    else:
        if not isleft:
            lx, ly = leftPos

            # Scroll left
            pyautogui.moveTo(lx, ly)
            pyautogui.click()
            isleft = True
            time.sleep(SCROLLTIMEOUT)
        x, y = getCoordsOfColor(list=list, color=closest)
        pyautogui.moveTo(x, y)
        pyautogui.click()


def getColorFromImage(x: int, y: int, image: Image.Image):
    return image.getpixel((x, y))


def clickScreenPixel(x, y, xrange, yrange, bounds):
    topLeft, bottomRight = bounds
    xstep = (bottomRight[0] - topLeft[0]) / xrange
    ystep = (bottomRight[1] - topLeft[1]) / yrange

    pyautogui.moveTo(topLeft[0] + xstep*x, topLeft[1] + ystep*y)
    pyautogui.click()


def askUserToSavePositions(leftButton, rightButton, leftColors, rightColors, combinedColors):
    # Ask the user if they want to save the positions if so save it to json
    inp = input("Do you want to save the positions? (y/n) ")
    if inp == "y":
        filename = input("What is the name of the settings file? ")
        with open(f"settings/{filename}.json", "w") as f:
            json.dump({"leftButton": leftButton, "rightButton": rightButton, "leftColors": leftColors,
                      "rightColors": rightColors, "combinedColors": combinedColors}, f)


def askUserToLoadPositions():
    # Ask the user if they want to load the positions if so load it from json
    filename = input("What is the name of the settings file? ")
    with open(f"settings/{filename}.json", "r") as f:
        data = json.load(f)
    return data


def main():
    global isleft
    inp = input("Do you want to load positions? (y/n) ")
    image = loadUsersImage()
    if inp == "y":
        data = askUserToLoadPositions()
        leftButton = data["leftButton"]
        rightButton = data["rightButton"]
        leftColorsAndPositions = data["leftColors"]
        rightColorsAndPositions = data["rightColors"]
        combinedColors = data["combinedColors"]
        input("Please scroll right and press enter ")
        isleft = False
    else:
        leftColorsAndPositions = getColorsAndPositions([], "left")
        rightColorsAndPositions = getColorsAndPositions([], "right")
        combinedColors = getCombinedColorsList(
            leftColorsAndPositions, rightColorsAndPositions)
        leftButton = getButton("left")
        rightButton = getButton("right")
        isleft = False

    bounds = getScreenBounds()
    scalefactor = int(
        input("What scale factor do you want to use? Lower = More resolution"))
    xrange, yrange = getRanges(scalefactor, image)

    for x in range(xrange):
        for y in range(yrange):
            target = getColorFromImage(x * scalefactor, y * scalefactor, image)
            selectClosestColor(combinedColors, target,
                               leftColorsAndPositions, rightColorsAndPositions,  rightButton, leftButton)
            clickScreenPixel(x, y, xrange, yrange, bounds)
    if inp != "y":
        askUserToSavePositions(leftButton, rightButton, leftColorsAndPositions,
                               rightColorsAndPositions, combinedColors)


if __name__ == "__main__":
    main()
