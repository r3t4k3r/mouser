import tkinter as tk

class Overlay(tk.Tk):
    def __init__(self, *a, **kw):
        tk.Tk.__init__(self, *a, **kw)
        self._set_window_attrs()
        self.set_transparency()

    def _set_window_attrs(self):
        self.title("Overlay")
        self.geometry("10x10+100+100")        # Force window focus
        self.focus_force()
        self.wm_attributes("-topmost", True)        # remove borders to prevent resizing
        self.overrideredirect(True)        # window vars:
        self.offset_x, self.offset_y = None, None        # bind the functions
        self.bind("<Button-1>", self.on_mouse_click)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_rel)

    def set_transparency(self):
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.config(highlightthickness=0)
        # self.canvas.create_oval(0, 0, 10, 10, fill="green", outline="green")
        self.canvas.create_polygon(0, 0, 0, 10, 10,10, 10, 0, fill="red", outline="red")
        # self.wm_attributes("-transparentcolor", "black")

    def on_mouse_click(self, event):
        self.offset_x = self.winfo_pointerx() - self.winfo_rootx()
        self.offset_y = self.winfo_pointery() - self.winfo_rooty()

    def on_mouse_drag(self, event):
        if None not in (self.offset_x, self.offset_y):
            new_window_x = self.winfo_pointerx() - self.offset_x
            new_window_y = self.winfo_pointery() - self.offset_y
            self.geometry("+%d+%d" % (new_window_x, new_window_y))

    def on_mouse_rel(self, event):
        self.offset_x, self.offset_y = None, None

    def run(self):
        self.mainloop()# driver code

if __name__ == "__main__":
    Overlay().run()
