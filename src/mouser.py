import evdev
from copy import deepcopy
from evdev import UInput
import mouse
import time
import argparse
import os

def evdev_list():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(f"path: {device.path}, name: {device.name}, phys: {device.phys}")

def evdev_run(self, args: argparse.Namespace):
    mouse_abs = list(mouse.get_position())
    mouse_drag = False

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
        os.exit(1)

    if device is None:
        print("not found device with provided name")
        os.exit(1)

    print(f'started with device: {device.path} ({device.name})')
    print('cursor position:', mouse_abs)
    self.geometry(f"10x10+{mouse_abs[0]}+{mouse_abs[1]}")

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
                    mouse_drag = True
                    mouse.move(mouse_abs[0]-1, mouse_abs[1])
                    time.sleep(0.001)
                if event.value == 0:
                    mouse_drag = False
                    self.deiconify()

            if event.code == 273: # RMB
                if event.value == 1:
                    # hide window
                    self.withdraw()
                    mouse.move(mouse_abs[0]-1, mouse_abs[1])
                    time.sleep(0.001)

                    # send event to Virtual device and execute
                    output_device.write_event(event)
                    output_device.syn()

                    # show window
                    time.sleep(0.001)
                    self.deiconify()

            # middle button click
            if event.code == 274 and event.value == 1:
                mouse.move(mouse_abs[0]-1, mouse_abs[1])
                continue

            output_device.write_event(event)
            output_device.syn()

        elif event.type == 2: # mouse start move
            # print("code:", event.code, "value:", event.value)
            if event.code == 0: # horizontal
                if mouse_drag: # twice
                    mouse_abs[0] = max(0, mouse_abs[0]+event.value*2)
                else:
                    mouse_abs[0] = max(0, mouse_abs[0]+event.value)
            elif event.code == 1: # vertical
                if mouse_drag: # twice
                    mouse_abs[1] = max(0, mouse_abs[1]+event.value*2)
                else:
                    mouse_abs[1] = max(0, mouse_abs[1]+event.value)
            elif event.code == 11 or event.code == 8: # scroll
                output_device.write_event(event)
                output_device.syn()

            if mouse_drag:
                output_device.write_event(event)
                output_device.write(0,0,0)
                output_device.syn()

            self.geometry(f"10x10+{mouse_abs[0]}+{mouse_abs[1]}")
            # self.keep_top()
        elif event.type == 4: # hold
            pass
        elif event.type == 0: # mouse move finish?
            pass
        else:
            print('unknown event:', event.type, event)

    device.ungrab()
    output_device.close()
