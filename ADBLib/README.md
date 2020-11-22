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

| Class      | Arguments                   | Description                                             |
|------------|-----------------------------|---------------------------------------------------------|
| SmartPhone | ADB_Path [, index = 0]      | Open ADB and select device, default selected device : 0 |
| Destroy    | ø                           | Destroy class, and remove remote files on android       |

| Class Settings | Arguments | Description                       |
|----------------|-----------|-----------------------------------|
| GetDevices     | ø         | Get all devices name              |
| SetDevice      | index     | Select an other device            |
| SetOffset      | x, x      | Add offset to calibrate functions |
| GetEventScreen | ø         | Get name of the screen            |

| Functions               | Arguments                   | Description                                                                           |
|-------------------------|-----------------------------|---------------------------------------------------------------------------------------|
| Press                   | x, y [, d = 1]              | Press the screen in (x, y) for d seconds                                              |
| Swipe                   | coords                      | Navigates the screen from point to point                                              |
| WriteText               | text                        | Simulation of smatphone keyboard                                                      |
| TakeScreenshot          | [debug = False]             | Take a screenshot and return image as CV2 Image (debug mode show details of transfer) |
| TakeScreenshotWithPress | x, y [, debug = False]      | Touch screen, take a screenshot and return image as CV2 Image                         |

| Arguments | Type                       |
|-----------|----------------------------|
| ADB_Path  | String                     |
| index     | Int                        |
| x         | Int                        |
| y         | Int                        |
| d         | Float                      |
| coords    | list of elements*          |
| element*  | list of 3 vars : [x, y, d] |
| text      | String                     |
| debug     | Bool                       |

## Example
```Python
from ADBLib import SmartPhone as SP

myPhone = SP()

myPhone.Press(500, 800) # Press screen in (500, 800)

# Starts and waits at the point (600, 822) for 0 seconds,
# then takes 0.5 seconds to go to the point (311, 922) and so on...
myPhone.Swipe([[ 600, 822, 0 ], [ 311, 922, 0.5 ], [ 500, 500, 1 ], [ 1000, 1000, 0.1 ]])

myPhone.TakeScreenshot().show() # Take Screenshot and show it
with myPhone.TakeScreenshot() as img:
    # Here, img is a PIL.Image format
    print(img.size)
    ...

myPhone.Destroy()
```

## Download
* [Download Python](https://www.python.org/)
* [Download ADB](https://www.frandroid.com/android/rom-custom-2/403222_comment-telecharger-les-outils-adb-et-fastboot-sur-windows-macos-et-linux)
* Download PIL
```
pip3 install Pillow
```

## Sources
* [ADB Commands Source 1 (medium.com)](https://medium.com/@minamimunakata/how-to-take-a-screenshot-on-android-with-adb-on-windows-pc-d52f7603b1d2)
* [ADB Record / Replay events (github : Cartucho)](https://github.com/Cartucho/android-touch-record-replay)