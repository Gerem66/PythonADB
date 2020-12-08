import os

def SaveMove(self):
    print("[!] Ctrl-C to end recording")
    os.system("{}adb -s {} exec-out getevent -t {} > recorded_touch_events.txt".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], self.EVENTSCREEN))
    exit(0)

def SendMove(self):
    if not os.path.isfile("recorded_touch_events.txt"):
        print("You must record events before send it.")
        exit(0)
    self.ADB("push recorded_touch_events.txt /data/local/tmp/", quiet=True)
    self.ADB("shell /data/local/tmp/sendevent-arm64 {} /data/local/tmp/recorded_touch_events.txt".format(self.EVENTSCREEN), quiet=True)
    self.ADB("shell rm /data/local/tmp/recorded_touch_events.txt", quiet=True)

def SaveMove():
    print("[!] Ctrl-C to end recording")
    os.system("adb exec-out getevent -t /dev/input/event2 > recorded_touch_events.txt")
    exit(0)

SaveMove()