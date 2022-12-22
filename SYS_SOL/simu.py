try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


import math
# class installations de toutes les planetes


class Planets(object):
    def __init__(self):
        self.r = None
        self.x = 500
        self.y = 300

    def install(self, canvas):
        self.r = 10
        for i in range(2):
            Planet().install(canvas, self.r, self.x, self.y)
            self.x = self.x + 150


# class trajectoires des planetes
class Path(object):
    def __init__(self):
        self.id_path = None
        self.r = 30
        self.ls_Path = []
        self.angle = 0

    # installation trajectoire
    def install(self, canvas, id_planet):
        x1, y1, x2, y2 = canvas.coords(id_planet)
        # si pas le soleil 1 seule trajectoire associé sinon 8 trajectoire
        if id_planet != 1:
            self.id_path = canvas.create_oval(
                x1-self.r, y1-self.r, x2+self.r, y2+self.r)
        else:
            for i in range(8):
                self.id_path = canvas.create_oval(
                    x1-self.r, y1-self.r, x2+self.r, y2+self.r)
                self.update(canvas, self.r, x1, y1)

        self.update(canvas, self.r, x1, y1)

    def update(self, canvas, r, x, y):
        x = x + r * math.cos(self.angle)
        y = y + r * math.sin(self.angle)
        print(self.angle)

        # Mise à jour de l'angle
        self.angle = self.angle + 0.1

        # Effacement du canevas
        canvas.coords(self.id_path, x-r, y-r, x+r, y+r)

        # Dessin des cercles
        Planets().install(canvas)

# class Planet création planete


class Planet(object):
    def __init__(self):
        self.id_planet = None
        self.ls_planet = []

    def install(self, canvas, r, x, y):
        self.id_planet = canvas.create_oval(
            x-r, y-r, x+r, y+r, fill="orange")
        Path().install(canvas, self.id_planet)

    def get_id_planet(self):
        return self.id_planet


class SYS_SOL(object):
    def __init__(self, frame):
        width = 1000
        height = 600
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=width,
                                height=height, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)

    def get_canvas(self):
        return self.canvas

    def animation(self):
        Planets().install(self.canvas)

    def start_animation(self):
        self.frame.after(30, self.animation)


class Simulation(object):
    # main simu
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Système solaire")
        height = 600
        width = 800
        self.frame = tk.Frame(self.root, height=height, width=width)
        self.frame.pack(side="top", fill="both")
        self.simu = SYS_SOL(self.frame)
        self.canvas = self.simu.get_canvas

    def play(self):
        self.simu.start_animation()
        self.root.mainloop()


Simulation().play()
