# PythonADB

## Use
1. You must have this git project, **Python**, **ADB** and **OpenCV2** (download links in sources)
> Tested on Python 3.8, ADB 8.1.0, OpenCV 4.2.0
2. Include in project
```Python
from ADBLib import SmartPhone as SP
```
3. Initalisation with ADB path
* Windows
```Python
myPhone = SP(r"C:\Users\___\platform-tools")
```
* Linux
```Python
myPhone = SP()
```
4. Use all fonctions !!!

|                         | Arguments              | Args Type         | Returned Type  | Description                                                   |
|-------------------------|------------------------|-------------------|----------------|---------------------------------------------------------------|
| **Class**               |                        |                   |                |                                                               |
| SmartPhone              | ADB_Path [, index = 0] | Str, Int          | ø              | Open ADB and select device, default selected device : 0       |
| Destroy                 | ø                      |                   | ø              | Destroy class, and remove remote files on android             |
| **Class Settings**      |                        |                   |                |                                                               |
| GetDevices              | ø                      |                   | List of String | Get all devices name                                          |
| SetDevice               | index                  | Int               | ø              | Select an other device                                        |
| SetOffset               | x, x                   | Int, Int          | ø              | Add offset to calibrate functions                             |
| GetEventScreen          | ø                      |                   | String         | Get name of the screen                                        |
| **Class Functions**     |                        |                   |                |                                                               |
| Press                   | x, y [, d = 1]         | Int, Int[, Float] | ø              | Press the screen in (x, y) for d seconds                      |
| Swipe                   | coords                 | List of Elements* | ø              | Navigates the screen from point to point                      |
| WriteText               | text                   | String            | ø              | Simulation of smatphone keyboard                              |
| TakeScreenshot          | [debug = False]        | Bool              | CV2 Image      | Take a screenshot (debug mode show details of transfer)       |
| TakeScreenshotWithPress | x, y [, debug = False] | Int, Int[, Bool]  | CV2 Image      | Touch screen, take a screenshot and return image as CV2 Image |
| **Variables**           |                        |                   |                |                                                               |
| Elements*               |                        |                   |                | Format [ Int, Int, Float] : x, y, time in seconds             |

## Example
```Python
from ADBLib import SmartPhone as SP

myPhone = SP()

myPhone.Press(500, 800) # Press screen in (500, 800)

# Starts and waits at the point (600, 822) for 0 seconds,
# then takes 0.5 seconds to go to the point (311, 922) and so on...
myPhone.Swipe([[ 600, 822, 0 ], [ 311, 922, 0.5 ], [ 500, 500, 1 ], [ 1000, 1000, 0.1 ]])

# Take and show screenshot
img = myPhone.TakeScreenshot()                                   # Take screenshot
img = cv2.resize(img, (int(len(img[0]) / 4), int(len(img) / 4))) # Resize : resolution / 4
cv2.imshow("test", img)                                          # Show popup with screenshot
cv2.waitKey(0)                                                   # Wait to press key
cv2.destroyAllWindows()                                          # Destroy window

myPhone.Destroy()
```

## Download

| Package | Windows | Linux (Debian) | Linux (Arch) | Other |
|---|---|---|---|---|
| Python | [Python](https://www.python.org/) | ``` sudo apt install python3 ``` | ``` sudo pacman -S python3 ``` |
| ADB | [ADB](https://www.frandroid.com/android/rom-custom-2/403222_comment-telecharger-les-outils-adb-et-fastboot-sur-windows-macos-et-linux) | ``` sudo apt install adb ``` | ``` sudo pacman -S adb ``` |
| OpenCV2 | [OpenCV2](https://opencv.org/) | ``` sudo apt install python3-opencv ``` | Install package from this [git](https://aur.archlinux.org/opencv2.git) | ``` pip3 install opencv-python ``` |

## Sources
* [ADB Commands Source 1 (medium.com)](https://medium.com/@minamimunakata/how-to-take-a-screenshot-on-android-with-adb-on-windows-pc-d52f7603b1d2)
* [ADB Record / Replay events (github : Cartucho)](https://github.com/Cartucho/android-touch-record-replay)
* [MarkDown syntaxe (gitlab.com)](https://docs.gitlab.com/ee/user/markdown.html)
* [cv2 in VSCode error (github.com)](https://github.com/PyCQA/pylint/issues/2426)