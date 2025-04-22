import evdev
from copy import deepcopy
from evdev import UInput
import mouse
import time
import argparse
import sys
import random

def evdev_list():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(f"path: {device.path}, name: {device.name}, phys: {device.phys}")

def background(cursor, args: argparse.Namespace):
    position = deepcopy(cursor.mouse_abs)
    start = time.time()
    while True:
        time.sleep(0.05)
        end = time.time()
        time_diff = end - start

        new_position = cursor.mouse_abs

        # no movement more then 300ms
        if new_position[0] == position[0] and new_position[1] == position[1] and time_diff > args.focus_delay:
            t = deepcopy(new_position)
            position = [t[0]-1, t[1]-1]
            mouse.move(new_position[0]-1, new_position[1]-1)
            start = time.time()
        # no movement
        elif new_position[0] == position[0] and new_position[1] == position[1]:
            pass
        else:
            position = deepcopy(new_position)
            start = time.time()

def evdev_run(self, cursor, args: argparse.Namespace):
    cursor.mouse_abs = list(mouse.get_position())
    mouse_drag = False

    self.geometry(f"10x10+{cursor.mouse_abs[0]}+{cursor.mouse_abs[1]}")

    device = None
    # if --device provided
    if args.device:
        device = evdev.InputDevice(args.device)

    # if --name provided
    elif args.name:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for d in devices:
            if args.name in d.name:
                if args.phys:
                    # if --phys provided
                    if args.phys in d.phys:
                        device = d
                    else:
                        continue
                else:
                    device = d
                break
    else:
        print("please provide --device or --name argument, devices list can be showed using --list")
        sys.exit(1)

    if device is None:
        print("not found device with provided name")
        sys.exit(1)

    print(f'started with device: {device.path} ({device.name})')
    print('cursor position:', cursor.mouse_abs)
    self.geometry(f"10x10+{cursor.mouse_abs[0]}+{cursor.mouse_abs[1]}")

    # copy capabilities from original device
    cap = deepcopy(device.capabilities())

    # ecodes.EV_SYN(0) cannot be in the cap dictionary or the device will not be created.
    if cap.get(0):
        del cap[0]

    output_device = UInput(cap, name='Mouser', version=0x3) # type: ignore
    device.grab()

    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            # print('click event:', event)
            if event.code == 272: # onclick
                if event.value == 1:
                    self.withdraw() # hide window
                    mouse.move(cursor.mouse_abs[0]-1, cursor.mouse_abs[1])
                    time.sleep(random.randint(8, 16)/1000)
                    mouse_drag = True
                if event.value == 0:
                    mouse_drag = False
                    position = list(mouse.get_position())
                    mouse.move(position[0], position[1])
                    time.sleep(random.randint(8, 16)/1000)
                    self.deiconify()

            if event.code == 273: # RMB
                if event.value == 1:
                    # hide window
                    self.withdraw()
                    mouse.move(cursor.mouse_abs[0]-1, cursor.mouse_abs[1])
                    time.sleep(random.randint(8, 16)/1000)

                    # send event to Virtual device and execute
                    output_device.write_event(event)
                    output_device.syn()

                    # show window
                    time.sleep(random.randint(8, 16)/1000)
                    self.deiconify()

            # middle button click
            if event.code == 274:
                if event.value == 1:
                    self.withdraw() # hide window
                    mouse.move(cursor.mouse_abs[0]-1, cursor.mouse_abs[1])
                    time.sleep(random.randint(8, 16)/1000)
                    mouse_drag = True
                if event.value == 0:
                    mouse_drag = False
                    position = list(mouse.get_position())
                    mouse.move(position[0], position[1])
                    time.sleep(random.randint(8, 16)/1000)
                    self.deiconify()

            output_device.write_event(event)
            output_device.syn()

        elif event.type == 2: # mouse start move
            # print("code:", event.code, "value:", event.value)
            if event.code == 0: # horizontal
                if mouse_drag: # twice
                    cursor.mouse_abs[0] = max(0, cursor.mouse_abs[0]+event.value)
                else:
                    cursor.mouse_abs[0] = max(0, cursor.mouse_abs[0]+event.value)
            elif event.code == 1: # vertical
                if mouse_drag: # twice
                    cursor.mouse_abs[1] = max(0, cursor.mouse_abs[1]+event.value)
                else:
                    cursor.mouse_abs[1] = max(0, cursor.mouse_abs[1]+event.value)
            elif event.code == 11 or event.code == 8: # scroll
                output_device.write_event(event)
                output_device.syn()

            if mouse_drag:
                output_device.write_event(event)
                output_device.write(0,0,0)
                output_device.syn()

            self.geometry(f"10x10+{cursor.mouse_abs[0]}+{cursor.mouse_abs[1]}")
            self.keep_top()
        elif event.type == 4: # hold
            pass
        elif event.type == 0: # mouse move finish?
            pass
        else:
            print('unknown event:', event.type, event)

    device.ungrab()
    output_device.close()
