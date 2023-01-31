- Main video file located in ..\static\css_b1

Initial Setup 
-------------
1. Download and install python from https://www.python.org/downloads/ 
2. Download and install Visual Studio Code from https://code.visualstudio.com/download
3. Download and install Anaconda for python from https://www.anaconda.com/
4. Open Anaconda Navigator then launch VS Code
5. Open a new terminal and then write "cd" then the path of the folder containing requirements.txt
6. Then write the following code "pip install --no-index --find-links /path to dependencies directory/ -r requirements.txt"
7. In VS Code open the WebApp folder then open main.py
8. Check the LAN IP Adress of the device and update the following statement: bacnet = BAC0.connect(ip='')
