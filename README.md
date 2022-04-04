# Peardraw

Why actually put skill into drawing when you can have a script to it for you?

A little while ago I realized that I was really bad at Peardeck drawing. So I used the one tool that I had the skills to use, Python. With the powers of Python and this script you too can commit forgery or something. 

## Installation

* `python3 -m venv env` Make a virtual environment.
* `source env/bin/activate` (Mac and linux) `./env/Scripts/activate` (Windows) Activate the virtual environment.
* `pip install -r requirements.txt` Install the requirements.
Done!

## How to use
* Run DrawPD2.py
* You'll be asked if you want to open a settings file. This file isn't included by default so you probably want to say `n` the first time
* You'll now be asked what image file you want to open. This is the image you want to draw. Note that this is either the relative path to the image or the absolute path to the image. If you want to draw the same image a lot you might want to put it into the images folder and use the relative path like `images/image.png`
* Now the program will ask you if you to hover over and press enter for each color. It's recommended to open your terminal/code editor on one side of your screen/a seperate monitor. Make sure you have the terminal selected and then for each color in the peardeck color bar, press enter. When your done, type `n` and press enter.
* Now scroll to the other side and repeat the process.
* Hover over the left and right buttons, and press enter.
* You'll now be asked to set the screen bounds, this is the actual area of the screen that you are saying is valid for drawing on. This also determines the final shape of your image so if your image is a square you want your bounds to be atleasy roughly the square shaped.
* Last thing, the scale factor. This determines the "resolution" of your final image. Basically what percentage of the pixels from the original image will be drawn. Lower = better quality. Higher = faster run times. Note that peardeck is a bit slow so if you place too many pixels it'll start lagging. You can mostly counter this either by increasing `Pyautogui.PAUSE` or by increasing the scale factor. The first will increase the run time and the secound will decrease the actual total number of pixels drawn.
* Once the script finishes drawing you'll be asked if you want to save the settings. It's recomended to do this to avoid having to re-enter the settings every time you want to draw. Note that you have to have the browser taking up the same parts of the screen with the same zoom settings otherwise you might get some weird bugs.

### Disclaimer
This script has full control over your mouse. If something goes horribly wrong it's not my fault. If something is going wrong slam your mouse to the top left corner of your screen which should shutdown the script.