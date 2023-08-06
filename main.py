from PIL import ImageGrab, ImageChops, ImageStat
import time
import beepy
from datetime import datetime
import os

# SETTINGSCONFIGURATION ####
RMS_THRESHOLD = 20
DESTINATION_FOLDER = "./"
SECONDS_INTERVAL = 3 #SECONDS
############################

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
    filename = os.path.abspath(os.path.join(DESTINATION_FOLDER, filename))
    im.save(f"{filename}")
    beepy.beep(sound='ping')
    print(f"Image saved to {filename}")


if __name__ == "__main__":
    last_cap = None

    print("Process stared.")
    print(f"Output will be save in := '{os.path.abspath(DESTINATION_FOLDER)}'")
    print(f"RMS Threshold to trigger save := '{RMS_THRESHOLD}'")
    print(f"Repeat interval := '{SECONDS_INTERVAL} SECONDS'")
    print(f"Press Ctrl+C to quit/exit.\n\n")
    try:
        while True:
            im = ImageGrab.grab()
            if last_cap:
                stats = image_stats(im, last_cap)
                print(f"RMS: {stats.rms[0]}")
                if stats.rms[0] > RMS_THRESHOLD:
                    save_image(im)
                else:
                    print("No image saved. Nothing changed in screen display detected.")
            else:
                save_image(im)

            last_cap = im
            time.sleep(SECONDS_INTERVAL)

    except KeyboardInterrupt:
        print("Process completed.")
        exit(0)