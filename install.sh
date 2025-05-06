#!/bin/bash
pip3 install tkinter
pip3 install pyperclip
pip3 install os
pip3 install subprocess
pip3 install platform
echo 'If you have not changed the paths on line 8 yet, do it now!'
cat /path/to/pythonpad.txt > ~/.local/share/applications/pythonpad.desktop
echo 'Install complete!'
sudo restart
