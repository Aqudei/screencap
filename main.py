import os
import subprocess
import sys
import threading
import time
from datetime import datetime

import beepy
from PIL import ImageGrab, ImageChops, ImageStat
from pynput import keyboard

TOGGLE_HOTKEY = "<f8>"


def play_ping() -> None:
    subprocess.run(
        ["afplay", "/System/Library/Sounds/Ping.aiff"],
        check=False,
    )


def beep() -> None:
    if 'darwin' in str(sys.platform):
        target = play_ping
        kwargs = {}
    else:
        target = beepy.beep
        kwargs = {"sound": "ping"}
    threading.Thread(target=target, kwargs=kwargs, daemon=True).start()


def toggle_capture(capture_enabled: threading.Event) -> None:
    if capture_enabled.is_set():
        capture_enabled.clear()
        print("Capture paused.")
    else:
        capture_enabled.set()
        print("Capture resumed.")

# SETTINGSCONFIGURATION ####
RMS_THRESHOLD = 40
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
    beep()
    print(f"Image saved to {filename}")


if __name__ == "__main__":
    last_cap = None
    capture_enabled = threading.Event()
    capture_enabled.set()
    hotkey_listener = keyboard.GlobalHotKeys(
        {TOGGLE_HOTKEY: lambda: toggle_capture(capture_enabled)}
    )

    print("Process stared.")
    print(f"Output will be save in := '{os.path.abspath(DESTINATION_FOLDER)}'")
    print(f"RMS Threshold to trigger save := '{RMS_THRESHOLD}'")
    print(f"Repeat interval := '{SECONDS_INTERVAL} SECONDS'")
    print("Press F8 to pause/resume capture. Press Ctrl+C to quit.\n")

    hotkey_listener.start()
    try:
        while True:
            if not capture_enabled.is_set():
                time.sleep(SECONDS_INTERVAL)
                continue

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
    finally:
        hotkey_listener.stop()
        hotkey_listener.join()