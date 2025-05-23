import threading
import tkthread; tkthread.patch()
import tkinter as tk
import mouser
import argparse
import sys

class Cursror:
    mouse_abs: list[int]

    def __init__(self):
        self.mouse_abs = [0, 0]

class Overlay(tk.Tk):
    def __init__(self, *a, **kw):
        tk.Tk.__init__(self, *a, **kw)
        self._set_window_attrs()
        self.set_transparency()

    def _set_window_attrs(self):
        self.title("Overlay")
        self.keep_top()
        self.overrideredirect(True)
        self.offset_x, self.offset_y = None, None
        self.config(cursor="")
        self.geometry(f"10x10+100+100")

    def keep_top(self):
        self.focus_force()
        self.wm_attributes("-topmost", True)

    def set_transparency(self):
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.config(highlightthickness=0)
        self.canvas.create_polygon(0, 0, 0, 10, 10, 10, 10, 0, fill="red", outline="red")

    def run(self, args: argparse.Namespace):
        # show devices list and exit
        if args.list:
            mouser.evdev_list()
            return

        # start mouser
        cursor = Cursror()
        t = threading.Thread(target=mouser.evdev_run, args=(self, cursor, args))
        t1 = threading.Thread(target=mouser.background, args=(cursor, args))

        t.start()
        t1.start()

        # show gui
        self.mainloop()
        sys.exit(0)

        # t.join()
        # t1.join()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--device', help="mouse device, for example /dev/input/event16")
    p.add_argument('-n', '--name', help="substring for search in devices, for example 'E-Signal USB Gaming Mouse'")
    p.add_argument('-p', '--phys', help="substring for search in phys, if exists more then 1 device with the same name, you have to provide this argument (see --list)")
    p.add_argument('-l', '--list', help="just show devices list and exit", action='store_true')
    p.add_argument('-f', '--focus-delay', help="delay between cursor teleport", type=float, default=0.2)
    args = p.parse_args()

    Overlay().run(args)
