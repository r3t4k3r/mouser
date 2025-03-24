# mouser
Anti mouse tracking tool. You could prevent user identification using mouse movement fingerprinting.

You can read more information about this security risk on [Whonix WIKI](https://www.whonix.org/wiki/Keystroke_Deanonymization#Mouse_Fingerprinting) and [Wikipedia](https://en.wikipedia.org/wiki/Mouse_tracking)

# Usage
Software requires root permissions for working. (For grab device, and show device list, `kloak` do the same thing)

## Build
```bash
/scripts/init.sh # init venv and install requirements
/scripts/build.sh # build project using nuitka
```
`build.sh` script will create a static binary for linux, using `nuitka` (python compiller). If you doesnt' trust nuitka you can run software without it, using `sudo .venv/bin/python3 src/main.py -l`

## Help
```
usage: main.bin [-h] [-d DEVICE] [-n NAME] [-p PHYS] [-l]

options:
  -h, --help           show this help message and exit
  -d, --device DEVICE  mouse device, for example /dev/input/event16
  -n, --name NAME      substring for search in devices, for example 'E-Signal USB Gaming Mouse'
  -p, --phys PHYS      if more then 1 device with same name, you have to provide this argument (see --list)
  -l, --list           just show devices list and exit
```

## list
Start with get devices list using `--list` flag:
```bash
sudo ./main.bin -l
```

Result:
```
path: /dev/input/event26, name: input-remapper SONiX AK820 forwarded, phys: py-evdev-uinput
path: /dev/input/event25, name: E-Signal USB Gaming Mouse, phys: usb-0000:00:14.0-2/input1
path: /dev/input/event24, name: E-Signal USB Gaming Mouse Keyboard, phys: usb-0000:00:14.0-2/input1
path: /dev/input/event23, name: E-Signal USB Gaming Mouse, phys: usb-0000:00:14.0-2/input0
path: /dev/input/event22, name: SONiX AK820, phys: usb-0000:00:14.0-1/input1
path: /dev/input/event21, name: SONiX AK820 Mouse, phys: usb-0000:00:14.0-1/input1
path: /dev/input/event19, name: SONiX AK820 Keyboard, phys: usb-0000:00:14.0-1/input1
path: /dev/input/event18, name: SONiX AK820 System Control, phys: usb-0000:00:14.0-1/input1
path: /dev/input/event17, name: SONiX AK820 Consumer Control, phys: usb-0000:00:14.0-1/input1
path: /dev/input/event16, name: SONiX AK820, phys: usb-0000:00:14.0-1/input0
path: /dev/input/event13, name: HDA Intel PCH HDMI/DP,pcm=8, phys: ALSA
path: /dev/input/event12, name: HDA Intel PCH HDMI/DP,pcm=7, phys: ALSA
path: /dev/input/event11, name: HDA Intel PCH HDMI/DP,pcm=3, phys: ALSA
path: /dev/input/event10, name: HDA Intel PCH Headphone, phys: ALSA
path: /dev/input/event9, name: HDA Intel PCH Mic, phys: ALSA
path: /dev/input/event8, name: TPPS/2 IBM TrackPoint, phys: rmi4-00.fn03/serio0/input0
path: /dev/input/event7, name: Synaptics TM3276-022, phys: rmi4-00/input0
path: /dev/input/event6, name: Video Bus, phys: LNXVIDEO/video/input0
path: /dev/input/event4, name: ThinkPad Extra Buttons, phys: thinkpad_acpi/input0
path: /dev/input/event5, name: PC Speaker, phys: isa0061/input0
path: /dev/input/event3, name: AT Translated Set 2 keyboard, phys: isa0060/serio0/input0
path: /dev/input/event2, name: Power Button, phys: LNXPWRBN/button/input0
path: /dev/input/event1, name: Lid Switch, phys: PNP0C0D/button/input0
path: /dev/input/event0, name: Sleep Button, phys: PNP0C0E/button/input0
```

## Running
In my case i need to start `/dev/input/event23`:
```bash
sudo ./main.bin -n "E-Signal USB Gaming Mouse" -p "input0"
```

I also can use `--device` flag for it
```bash
sudo ./main.bin -d /dev/input/event23
```

# Daily using
## Workflow
After running, you will see a red square on the your screen. This is a your new cursor, apps can't track it, they tracks your real cursor. You can move it like a real cursor. For work with app you have to use mostly **LMB**, **MMB**, and **RMB**. For click you just press **LMB**, selecting is also working, this action will teleport your real cursor to red square position and click it. Some actions in web browsers/software could be avaliable only after hover on it without clickig, for do it using `mouser` you have to press **MMB**, this button will teleport your cursor to red-poiter position without clicking.

## Buttons binding
- **Middle Mouse Button** will teleport cursor to pointer position
- **Left Mouse Button** will teleport cursor to pointer position and click it
- **Right Mouse Button** will teleport cursor to pointer position and use MBR
- **Other buttons** works like on original device

# Known Bugs
- Some context menus can hide pointer (i don't know how to fix it now). In this case u can use **Middle Mouse Button** for detect cursor position.
- Discrepancies between the real cursor and the emulated cursor when selecting/transferring (Maybe problem with mouse acceleration, i'm not sure)
- X11 supports only, doesn't work with XWayland (python library coudn't detect mouse position correctly)

# Demo Video
https://webm.red/view/iG9Q.webm
