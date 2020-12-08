#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

SCREEN = "/dev/input/event4"

# Upload files
os.system("adb push sendevent-arm64 /data/local/tmp/")
os.system("adb push events /data/local/tmp/")

# Add permissions (BUT DOESN'T WORKS !!!)
os.system("adb shell chmod 777 /data/local/tmp/sendevent-arm64")
os.system("adb shell chmod 777 /data/local/tmp/events")

# Execute pattern (circle)
os.system("adb exec-out /data/local/tmp/sendevent-arm64 {} /data/local/tmp/events".format(SCREEN))

# Remove files
os.system("adb shell rm /data/local/tmp/sendevent-arm64")
os.system("adb shell rm /data/local/tmp/events")