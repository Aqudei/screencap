from uuid import uuid4
from PIL import ImageGrab, ImageChops, ImageStat
import time
import beepy
from datetime import datetime
import os

THRESHOLD = 20
DATA_DIR = "./"


def image_stats(im1, im2):
    """
    docstring
    """
    gray1 = im1.convert("L")
    gray2 = im2.convert("L")
    diff = ImageChops.difference(gray1, gray2)
    return ImageStat.Stat(diff)


def save_image(im):
    filename = f"Capture-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
    filename = os.path.abspath(os.path.join(DATA_DIR, filename))
    im.save(f"{filename}")
    beepy.beep(sound='ping')
    print(f"Image saved to {filename}")


if __name__ == "__main__":
    last_cap = None

    try:
        while True:
            im = ImageGrab.grab()
            if last_cap:
                stats = image_stats(im, last_cap)
                if stats.rms[0] > THRESHOLD:
                    save_image(im)
            else:
                save_image(im)

            last_cap = im
            time.sleep(5)

    except KeyboardInterrupt:
        exit(0)
