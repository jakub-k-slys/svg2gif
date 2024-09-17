#!/usr/bin/python3

import contextlib
import glob
import os
import re
import shutil
import sys
from PIL import Image
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

if len(sys.argv) != 2:
    raise Exception("Usage: python svg2gif.py <SVG_file>")
FILE_NAME = sys.argv[1]
ABSOLUTE_FILE_PATH = os.getcwd()

SCREENSHOTS_PER_SECOND = 24
total_time_animated = 1.0

if not os.path.exists("_screenshots"):
    os.makedirs("_screenshots")

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options)
driver.get(f"file:///{FILE_NAME}")

total_screenshots = int(SCREENSHOTS_PER_SECOND * (total_time_animated * 2))
for i in range(total_screenshots):
    driver.get_screenshot_as_file(f"_screenshots/{i}.png")

driver.close()
driver.quit()

fp_in = "_screenshots/*.png"
fp_out = f'{FILE_NAME.replace(".svg", ".gif")}'

with contextlib.ExitStack() as stack:
    files = glob.glob(fp_in)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    imgs = (stack.enter_context(Image.open(f))
            for f in files)
    img = next(imgs)
    img.save(fp=fp_out,
             format='GIF',
             append_images=imgs,
             save_all=True,
             duration=100,
             loop=0)

shutil.rmtree("_screenshots")
