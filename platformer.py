__title__ = "platformer"
__author__ = "nekitdev"
__copyright__ = "Copyright 2020-2021 nekitdev"
__license__ = "MIT"
__version__ = "0.1.5"

import math
import time
import gd.memory
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
Geometry Dash Platformer Mod (GDPM) v{__version__} (Edited for GDPS 2.2 PC).
It works at any level, just click on the specified controls!
Created using gd.py (https://github.com/nekitdev/gd.py)
"""

how_to = """
 Controls:
     Right/d     -> Move forward.
     Left/a      -> Move back.
     A & D controls only suports english letters!
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
# noclip flag
noclip_enabled = False
# player rotation flag
rotation_unlocked = False
# size pricision, can be changed for more precise player size
size_precision = 1
# set speed value to default speed
speed_value = default_speed
# setup speed values
speed_values = [speed.value for speed in gd.api.SpeedConstant]
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

    size = round(memory.get_size(), size_precision)  # get current size
    # reflect speed value update (if went through speed changer)
    speed_value = round(memory.get_speed_value(), 1) or speed_value

    if memory.is_in_level() and key == Key.tab:  # if tab was pressed
        try:
            speed_index = speed_values.index(
                abs(speed_value)
            )  # get current speed index
        except ValueError:  # just in case
            speed_index = 0

        speed_index = (speed_index + 1) % len(
            speed_values
        )  # get next value (jump back if last)

        speed_value = math.copysign(speed_values[speed_index], speed_value)
        color = colors[speed_index]  # pick color according to the speed

        if (
            memory.get_speed_value()
        ):  # if player is moving, we can update speed on the fly
            memory.set_speed_value(speed_value)  # set speed value

        print(
            color + f"Speed changed to #{speed_index} ({abs(speed_value)})" + Fore.RESET
        )

    # arrow
    elif memory.is_in_level() == True and memory.gamemode.value == 0 and key == Key.right:  # if gamemode = 0 and right arrow or d was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif memory.is_in_level() == True and memory.gamemode.value == 0 and key == Key.left:  # if gamemode = 0 and left arrow or a  was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif memory.is_in_level() == True and key == Key.right:  # if right arrow or d was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value

    elif memory.is_in_level() == True and key == Key.left:  # if left arrow or a was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value

    # a or d
    elif memory.is_in_level() == True and memory.gamemode.value == 0 and key == KeyCode(char='d'):  # if gamemode = 0 and right arrow or d was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif memory.is_in_level() == True and memory.gamemode.value == 0 and key == KeyCode(char='a'):  # if gamemode = 0 and left arrow or a  was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif memory.is_in_level() == True and key == KeyCode(char='d'):  # if right arrow or d was pressed 
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif memory.is_in_level() == True and key == KeyCode(char='a'):  # if left arrow or a was pressed 
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value
        memory.player_unlock_jump_rotation()

    elif key == Key.esc:
        memory.player_unlock_jump_rotation()


    else:  # other key
        pass  # do nothing



def on_release(key: Union[str, Key]) -> bool:
    if key in {Key.left, Key.right, KeyCode(char='d'), KeyCode(char='a')}:  # if left/right arrow or a/d was released
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

        print("Waiting for Geometry Dash...")

        while not reload_memory():  # wait until GD is opened
            time.sleep(1)

        print("Found Geometry Dash.")

        # start memory reloading thread
        memory_reload_thread.start()


        # join the listener into main thread, waiting for it to stop
        listener.join()
        memory_reload_thread.join()

        print("Geometry Dash is closed.")

if __name__ == "__main__":
    main()