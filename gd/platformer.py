__title__ = "platformer"
__author__ = "nekitdev"
__copyright__ = "Copyright 2020-2021 nekitdev"
__license__ = "MIT"
__version__ = "0.1.5 (v1.4 - Edited for GDPS 2.2 PC)"

# change keyboard layout
import py_win_keyboard_layout
py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

import math
import time
import gd
import threading  # used for listening to events not related to keyboard
from typing import Union
from colorama import Fore  # type: ignore  # no typehints
import gd  # type: ignore  # no typehints
from pynput.keyboard import Key, Listener  # type: ignore  # no typehints
from pynput.keyboard import KeyCode
import ctypes


ctypes.windll.kernel32.SetConsoleTitleA(b"Geometry Dash Platformer Mod")

import colorama  # type: ignore  # no typehints

colorama.init()

info = f"""(c) {__copyright__}
Geometry Dash Platformer Mod (GDPM) v{__version__}.
Created using gd.py (https://github.com/nekitdev/gd.py)
"""

how_to = """
It works at any level, just click on the specified controls:

 Right/d     -> Move forward.
 Left/a      -> Move back.
 Any other   -> unlock rotation.
 A & D controls only suports latin letters!
"""

# process name, can be changed for different executable names, I guess
PROCESS_NAME = "GDPS-2.2-by-user666"  # no need for ".exe"
# setup colors for console
colors = [
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTRED_EX,
]
# set default speed to normal speed
default_speed = gd.api.SpeedConstant.NORMAL.value
# create gd.py memory object, without loading it (loaded when running)
memory = gd.memory.get_memory(PROCESS_NAME, load=False)
# set speed value to default speed
speed_value = default_speed
# setup speed values
speed_values = [speed.value for speed in gd.api.SpeedConstant]
# smooth speed change delay a
sleepigo = 0.03

try:
    speed_values.remove(0.0)
except ValueError:
    pass


def reload_memory() -> bool:  # try to reload memory and return reload status
    try:
        memory.reload()
        return True
    except RuntimeError:
        return False

def listen_for_gd_closed(listener: Listener) -> bool:
    should_close = False

    while True:
        if reload_memory():
            should_close = False

        else:
            if should_close:
                break

            should_close = True

        time.sleep(0.1)

    listener.stop()

def on_press(key: Union[str, Key]) -> bool:  # handle key press
    global noclip_enabled, rotation_unlocked, speed_value
    # arrow/ad
    if memory.is_in_level() == True and memory.gamemode.value == 0 and key == Key.right or key == KeyCode(char='d'):  # if gamemode = 0 and right arrow or d was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation() # player_unlock_jump_rotation huh

    elif memory.is_in_level() == True and memory.gamemode.value == 0 and key == Key.left or key == KeyCode(char='a'):  # if gamemode = 0 and left arrow or a  was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation() # player_unlock_jump_rotation huh

    elif memory.is_in_level() == True and key == Key.right or key == KeyCode(char='d'):  # if right arrow or d was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value

    elif memory.is_in_level() == True and key == Key.left or key == KeyCode(char='a'):  # if left arrow or a was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value

    else:  # other key
        memory.player_unlock_jump_rotation() # player_unlock_jump_rotation huh


    
def on_release(key: Union[str, Key]) -> bool:
    if key in {Key.right, KeyCode(char='d')}:  # if left/right arrow or a/d was released
            memory.set_speed_value(0.5)  # set speed to 0.5
            time.sleep(sleepigo)
            memory.set_speed_value(0.4)  # set speed to 0.4
            time.sleep(sleepigo)
            memory.set_speed_value(0.2)  # set speed to 0.2
            time.sleep(sleepigo)
            memory.set_speed_value(0.1)  # set speed to 0.1
            time.sleep(sleepigo)
            memory.set_speed_value(0.05)  # set speed to 0.5
            time.sleep(sleepigo)
            memory.set_speed_value(0)  # set speed to 0
            memory.player_lock_jump_rotation()
    elif key in {Key.left, KeyCode(char='a')}:  # if left arrow or a was released
            memory.set_speed_value(-0.5)  # set speed to 0.5
            time.sleep(sleepigo)
            memory.set_speed_value(-0.4)  # set speed to 0.4
            time.sleep(sleepigo)
            memory.set_speed_value(-0.2)  # set speed to 0.2
            time.sleep(sleepigo)
            memory.set_speed_value(-0.1)  # set speed to 0.1
            time.sleep(sleepigo)
            memory.set_speed_value(-0.05)  # set speed to 0.5
            time.sleep(sleepigo)
            memory.set_speed_value(0)  # set speed to 0
            memory.player_lock_jump_rotation()

    else:  # other key
        pass  # do nothing

def main() -> None:
    print(info)  # show simple info
    print(how_to)  # show tutorial on what the keys do

    with Listener(on_press=on_press, on_release=on_release) as listener:
        # create memory reloading thread
        memory_reload_thread = threading.Thread(
            target=listen_for_gd_closed,
            args=(listener,),
            name="MemoryReloadThread",
            daemon=True,
        )

        print("Waiting for",PROCESS_NAME)

        while not reload_memory():  # wait until GD is opened
            time.sleep(1)

        print("Found",PROCESS_NAME)

        # start memory reloading thread
        memory_reload_thread.start()

        # join the listener into main thread, waiting for it to stop
        listener.join()
        memory_reload_thread.join()

        print("Geometry Dash is closed.")

if __name__ == "__main__":
    main()
