gd.platformer
=============

gd.platformer is a library that implements Geometry Dash Platformer Mod in Python.

Installing
----------

**Python 3.6 or higher is required**

To install the library, you can just run the following command:



    # Windows
    py -3 -m pip install -U gd.platformer

In order to install the library from source, you can do the following:



    $ git clone https://github.com/nekitdev/gd.platformer
    $ cd gd.platformer
    $ python -m pip install -U .

Running
-------

Running the app is quite simple.

You can either invoke it from python:



    import gd.platformer

    gd.platformer.main()

Or run a console command:



     python -m gd.platformer

    # OR

     gd.platformer

Building
--------

You can build an executable file from the ``gd/platformer.py`` file using *PyInstaller*:



     pyinstaller --onefile --exclude-module PIL --exclude-module numpy --exclude-module IPython --exclude-module Crypto --exclude-module lxml --icon=icon.ico gd/platformer.py

Generated executable will be in ``./dist`` folder.

Authors
-------

This project is mainly developed by `nekitdev <https://github.com/nekitdev>`_ and `Sapfirenko <https://github.com/Sapphire1ne>`_.
Player rotation lock/unlock patch by `cos8o <https://github.com/Cos8o>`_.
