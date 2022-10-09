
gd.platformer
=============

22-pc-gdps-platformer it's edited gd.platformer library that implements Geometry Dash Platformer Mod in Python.

I have added: the name of the window, lock player rotation at 0 speed, unlock player rotation when moving, game mode conditions for this (player rotation), support for A and D, smooth stops and more...

Installing
----------

**Python 3.6 or higher is required**

just download source code or exe and install it anywhere 

Running
-------

just run gd/platformer.py
or platformer.exe

Building
--------

You can build an executable file from the ``platformer.py`` file using *PyInstaller*:


```
pyinstaller --onefile --exclude-module PIL --exclude-module numpy --exclude-module IPython --exclude-module Crypto --exclude-module lxml platformer.py
```
Generated executable will be in ``./dist`` folder.

Authors
-------

This project is mainly developed by [nekitdev](https://github.com/nekitdev)  and [Sapfirenko](https://github.com/sapfirenko).
Player rotation lock/unlock patch by [cos8o](https://github.com/Cos8o).
[Bang1338](https://github.com/Bang1338) found a way to use the letters A and D.
