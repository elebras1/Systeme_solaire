try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

import math

# Création de la fenêtre
window = tk.Tk()
window.title("Système solaire")

# Chargement de l'image
img = tk.PhotoImage(file="Space.png")

# Création du canevas
canvas = tk.Canvas(window, height=800, width=800)
canvas.pack(side="top", fill="both")

# Ajout de l'image en arrière-plan du canevas
canvas.create_image(0, 0, image=img, anchor="nw")

# Deplacement planete


def update_coords(id_planet, r_path, angle, size_planet, speed_planet):
    x = 400
    y = 400
    r = size_planet
    r_traj = r_path + 60
    x = x + r_traj * math.cos(angle)
    y = y + r_traj * math.sin(angle)
    canvas.coords(id_planet, x-r, y-r, x+r, y+r)
    angle = angle + speed_planet
    canvas.after(50, update_coords, id_planet, r_path,
                 angle, size_planet, speed_planet)
    if id_planet == ls_planet[2]:
        update_satellite(id_planet)

# Deplacement satellite


def update_satellite(id_planet):
    global angle_sat
    x1, y1, x2, y2 = canvas.coords(id_planet)
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    r = 4
    r_traj = 25
    x = x + r_traj * math.cos(angle_sat)
    y = y + r_traj * math.sin(angle_sat)
    canvas.coords(id_sat, x-r, y-r, x+r, y+r)
    angle_sat = angle_sat + 0.2


# Initialisation des variables
x = 400
y = 400
r = 60
r_path = 20
angle = 0
ls_planet = []
ls_path = []
angles = [0] * 8
angle_sat = 0
x_space = 0
size_planet = [5, 14, 15, 9, 30, 25, 18, 18]
color_planet = ["Azure", "Tomato2", "Blue2",
                "OrangeRed3", "Wheat2", "BurlyWood3", "RoyalBlue1", "RoyalBlue3"]
speed_planet = [0.1, 0.05, 0.07, 0.06, 0.04, 0.03, 0.02, 0.01]

# creation soleil
id_sun = canvas.create_oval(x-r, y-r, x+r, y+r, fill="orange")

# Création trajectoire
for i in range(8):
    x1, y1, x2, y2 = canvas.coords(id_sun)
    canvas.create_oval(x1-r_path, y1-r_path, x2+r_path,
                       y2+r_path, outline=color_planet[i])
    ls_path.append(r_path)
    r_path = r_path + 40

# Création des planetes
for i in range(8):
    r = size_planet[i]
    r_path = 60 * i
    r_traj = r_path + 60
    x = 400 + r_traj * math.cos(angles[i])
    y = 400 + r_traj * math.sin(angles[i])
    id_planet = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color_planet[i])
    ls_planet.append(id_planet)
    print(id_planet)


# Appel de la fonction de mise à jour toutes les 50 millisecondes
for i in range(8):
    canvas.after(50, update_coords,
                 ls_planet[i], ls_path[i], angles[i], size_planet[i], speed_planet[i])

# Création satellite
x1, y1, x2, y2 = canvas.coords(ls_planet[2])
x = x1
y = y1
r = 4
r_traj = 30
x = x + r_traj * math.cos(angle)
y = y + r_traj * math.sin(angle)
id_sat = canvas.create_oval(x-4, y-4, x+4, y+4, fill="Lightgrey")

# Boucle principale de l'application
window.mainloop()
