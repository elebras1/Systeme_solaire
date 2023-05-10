try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

import math


class Movement(object):
    def __init__(self, canvas, id_sat, sys_sol):
        self.canvas = canvas
        self.angle_sat = 0
        self.x_origin = sys_sol.get_x_origin()
        self.y_origin = sys_sol.get_y_origin()
        self.id_sat = id_sat
        self.ls_planet = sys_sol.get_ls_planet()

    def update_planet(self, id_planet, r_path, angle, size_planet, speed_planet):
        r = size_planet
        r_traj = r_path + 60
        x = self.x_origin + r_traj * math.cos(angle)
        y = self.y_origin + r_traj * math.sin(angle)
        self.canvas.coords(id_planet, x-r, y-r, x+r, y+r)
        angle = angle + speed_planet
        self.canvas.after(50, self.update_planet, id_planet,
                          r_path, angle, size_planet, speed_planet)
        if id_planet == self.ls_planet[2]:
            self.update_satellite(self.id_sat, id_planet)

    def update_satellite(self, id_sat, id_planet):
        self.angle_sat
        x1, y1, x2, y2 = self.canvas.coords(id_planet)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        r = 4
        r_traj = 25
        x = x + r_traj * math.cos(self.angle_sat)
        y = y + r_traj * math.sin(self.angle_sat)
        self.canvas.coords(id_sat, x-r, y-r, x+r, y+r)
        self.angle_sat = self.angle_sat + 0.2


class Satellite(object):
    def __init__(self, canvas, angle):
        self.canvas = canvas
        self.angle = angle
        self.r = 4
        self.id_sat = None

    def install(self, id_planet):
        x1, y1, x2, y2 = self.canvas.coords(id_planet)
        x = x1
        y = y1
        r_traj = 30
        x = x + r_traj * math.cos(self.angle)
        y = y + r_traj * math.sin(self.angle)
        self.id_sat = self.canvas.create_oval(
            x-self.r, y-self.r, x+self.r, y+self.r, fill="Lightgrey")

    def get_id_sat(self):
        return self.id_sat


class Planet(object):
    def __init__(self, canvas, r, r_path, color_planet, angle, sys_sol):
        self.canvas = canvas
        self.r = r
        self.r_path = r_path
        self.color_planet = color_planet
        self.angle = angle
        self.sys_sol = sys_sol
        self.x_origin = self.sys_sol.get_x_origin()
        self.y_origin = self.sys_sol.get_y_origin()

    def install(self, i):
        self.r_path = 60 * i
        r_traj = self.r_path + 60
        x = self.x_origin + r_traj * math.cos(self.angle)
        y = self.y_origin + r_traj * math.sin(self.angle)
        id_planet = self.canvas.create_oval(
            x-self.r, y-self.r, x+self.r, y+self.r, fill=self.color_planet)
        self.sys_sol.add_planet(id_planet)


class Path(object):
    def __init__(self, canvas, r_path):
        self.canvas = canvas
        self.r_path = r_path

    def install(self, id_sun, color_planet):
        x1, y1, x2, y2 = self.canvas.coords(id_sun)
        self.canvas.create_oval(x1-self.r_path, y1-self.r_path,
                                x2+self.r_path, y2+self.r_path, outline=color_planet)


class Sys_Sol(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.x_origin = 400
        self.y_origin = 400
        self.r_sun = 60
        self.angle_sat = 0
        self.size_planet = [5, 14, 15, 9, 30, 25, 18, 18]
        self.color_planet = ["Azure", "Tomato2", "Blue2", "OrangeRed3",
                             "Wheat2", "BurlyWood3", "RoyalBlue1", "RoyalBlue3"]
        self.speed_planet = [0.1, 0.08, 0.07, 0.06, 0.04, 0.03, 0.02, 0.01]
        self.ls_path = []
        self.angle = [0] * 8
        self.ls_planet = []
        self.sat = Satellite(self.canvas, self.angle_sat)
        self.id_sat = None

    def get_x_origin(self):
        return self.x_origin

    def get_y_origin(self):
        return self.y_origin

    def get_ls_planet(self):
        return self.ls_planet

    def add_planet(self, id_planet):
        self.ls_planet.append(id_planet)

    def install(self):
        id_sun = self.canvas.create_oval(self.x_origin-self.r_sun, self.y_origin -
                                         self.r_sun, self.x_origin+self.r_sun, self.y_origin+self.r_sun, fill="orange")
        r_path = 20

        # installation des trajectoires
        for i in range(8):
            Path(self.canvas, r_path).install(id_sun, self.color_planet[i])
            self.ls_path.append(r_path)
            r_path = r_path + 40

        # installation des planetes
        for i in range(8):
            Planet(self.canvas, self.size_planet[i], r_path,
                   self.color_planet[i], self.angle[i], self).install(i)
            r_path = r_path + 40

        # installation du satellites
        self.sat.install(self.ls_planet[2])
        self.id_sat = self.sat.get_id_sat()

        # mouvement des planetes et satellites
        for i in range(8):
            self.canvas.after(50, Movement(self.canvas, self.id_sat, self).update_planet,
                              self.ls_planet[i], self.ls_path[i], self.angle[i], self.size_planet[i], self.speed_planet[i])

    def start_animation(self):
        self.install()


class Main(object):
    def __init__(self):
        self.running = True
        self.root = tk.Tk()
        self.root.title("Système solaire")

        # Chargement de l'image
        self.img = tk.PhotoImage(file="Space.png")

        # Création du canevas
        self.canvas = tk.Canvas(self.root, height=800, width=800)
        self.canvas.pack(side="top", fill="both")

        # Ajout de l'image en arrière-plan du canevas
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")

        self.simu = Sys_Sol(self.canvas)

        self.canvas.winfo_toplevel().bind("<Button-1>", self.click)

    def click(self, event):
        print("clic gauche")
        
    def play(self,):
        self.simu.start_animation()
        self.root.mainloop()


Main().play()
