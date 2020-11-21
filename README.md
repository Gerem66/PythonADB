# PythonADB

## Use
1. You must have this git project, Python, ADB and PIL (download links in sources)
> Tested on Python 3.8, Pillow 8.0.1, numpy 1.19.4
2. Include in project
```Python
from ADBLib import SmartPhone as SP
```
3. Initalisation with ADB path
```Python
myPhone = SP(r"C:\Users\___\platform-tools")
```
4. Use all fonctions !!!

| Function                | Arguments (int)             | Description                                                                           |
|-------------------------|-----------------------------|---------------------------------------------------------------------------------------|
| SmartPhone (class)      | (str)ADB Path [, index = 0] | Open ADB and select device, default selected device : 0                               |
| GetDevices              | ø                           | Get all devices name                                                                  |
| SetDevice               | index                       | Select an other device                                                                |
| SetOffset               | x, x                        | Add offset to calibrate functions                                                     |
| Press                   | x, y                        | TouchScreen at x, y position                                                          |
| LongPress               | x, y [, d = 1000]           | Press the screen in (x, y) for d milliseconds                                         |
| Swipe                   | x1, y1, x2, y2 [, d = 1000] | Swipe the screen from (x1, y1) to (x2, y2) during d milliseconds                      |
| WriteText               | text                        | Simulation of smatphone keyboard                                                      |
| TakeScreenshot          | [debug = False]             | Take a screenshot and return image as CV2 Image (debug mode show details of transfer) |
| TakeScreenshotWithPress | x, y [, debug = False]      | Touch screen, take a screenshot and return image as CV2 Image                         |
| SaveMove                | ø                           | Save input screen events                                                              |
| SendMove                | ø                           | Send input screen events                                                              |

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

## To Do
- [ ] swipe en 3 temps 
- [ ] Revoir méthode pour trouver pokemon pokestop et arène
- [ ] arène (pokestop)
- [ ] pokestop
- [ ] repenser manière capter pokemon OU revoir filtre
- [ ] enlever le personnage pour pas appuyer dessus
- [ ] rond blanc capture nuit
- [ ] rajouter un moyen de savoir quand c'est mode nuit
- [ ] filtrer cercle couleur pour déterminer quel ball prendre
- [ ] encens fait beuger les filtres
- [ ] montgolfiere team rocket
- [ ] combat team rocket
- [ ] pokemon pas au centre terrain swipe 3 temps

## Sources
* [Download ADB](https://www.frandroid.com/android/rom-custom-2/403222_comment-telecharger-les-outils-adb-et-fastboot-sur-windows-macos-et-linux)
* Download PIL
```
pip3 install Pillow
```
* [ADB Commands Source 1 (medium.com)](https://medium.com/@minamimunakata/how-to-take-a-screenshot-on-android-with-adb-on-windows-pc-d52f7603b1d2)
* [ADB Commands Source 2 (stackoverflow)](https://stackoverflow.com/questions/11142843/how-can-i-use-adb-to-send-a-longpress-key-event)
* [ADB Commands Source 3 (althority.com)](http://www.althority.com/adb_shell_input/)
* [ADB Record / Replay events](https://github.com/Cartucho/android-touch-record-replay)