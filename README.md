# PythonADB

## Use
1. Download git and adb
2. Include in project
```Python
from ADBLib import SmartPhone as SP
```
3. Initalisation with ADB path
```Python
myPhone = SP(r"C:\Users\___\platform-tools")
```
4. Use all fonctions !!!
| Function  | Arguments                | Description                                                      |
| --------- | ------------------------ | ---------------------------------------------------------------- |
| Press     | (int)x, (int)y           | TouchScreen at x, y position                                     |
| LongPress | (int)x, (int)y, (int)d   | Press the screen in (x, y) for d milliseconds                    |
| Swipe     | x1, y1, x2, y2, duration | Swipe the screen from (x1, y1) to (x2, y2) during d milliseconds |


## Sources
* [Download ADB](https://www.frandroid.com/android/rom-custom-2/403222_comment-telecharger-les-outils-adb-et-fastboot-sur-windows-macos-et-linux)
* [ADB Commands Source 1 (medium.com)](https://medium.com/@minamimunakata/how-to-take-a-screenshot-on-android-with-adb-on-windows-pc-d52f7603b1d2)
* [ADB Commands Source 2 (stackoverflow)](https://stackoverflow.com/questions/11142843/how-can-i-use-adb-to-send-a-longpress-key-event)