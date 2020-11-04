# PythonADB

## Use
1. Download this git, ADB and PIL (in sources)
2. Include in project
```Python
from ADBLib import SmartPhone as SP
```
3. Initalisation with ADB path
```Python
myPhone = SP(r"C:\Users\___\platform-tools")
```
4. Use all fonctions !!!

| Function           | Arguments                | Description                                                      |
|--------------------|--------------------------|------------------------------------------------------------------|
| SmartPhone (class) | ADB Path [, index = 0]   | Open ADB and select device, default selected device : 0          |
| GetDevices         | ø                        | Get all devices name                                             |
| SetDevice          | (int) index              | Select an other device                                           |
| Press              | (int)x, (int)y           | TouchScreen at x, y position                                     |
| LongPress          | (int)x, (int)y, (int)d   | Press the screen in (x, y) for d milliseconds                    |
| Swipe              | x1, y1, x2, y2, duration | Swipe the screen from (x1, y1) to (x2, y2) during d milliseconds |
| TakeScreenshot     | ø                        | Take a screenshot and return image as PIL.Image                  |

## Example

```Python
from ADBLib import SmartPhone as SP

myPhone = SP("path_to_ADB")

myPhone.Press(500, 800) # Press screen in (500, 800)
myPhone.TakeScreenshot().show() # Take Screenshot and show it
with myPhone.TakeScreenshot() as img:
    # Here, img is a PIL.Image format
    print(img.size)
    ...
```

## Sources
* [Download ADB](https://www.frandroid.com/android/rom-custom-2/403222_comment-telecharger-les-outils-adb-et-fastboot-sur-windows-macos-et-linux)
* Download PIL
```
pip3 install Pillow
```
* [ADB Commands Source 1 (medium.com)](https://medium.com/@minamimunakata/how-to-take-a-screenshot-on-android-with-adb-on-windows-pc-d52f7603b1d2)
* [ADB Commands Source 2 (stackoverflow)](https://stackoverflow.com/questions/11142843/how-can-i-use-adb-to-send-a-longpress-key-event)
* [ADB Commands Source 3 (althority.com)](http://www.althority.com/adb_shell_input/)