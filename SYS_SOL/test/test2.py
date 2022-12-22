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

# Création du canevas
canvas = tk.Canvas(window, height=800, width=800)
canvas.pack(side="top", fill="both")

# Fonction qui met à jour les coordonnées du cercle
def update_coords(id_planet, r_path):
    global angle
    x = 400
    y = 400
    r = 15
    #r_traj = r_path + r * 2
    x = x + r_path * math.cos(angle)
    y = y + r_path * math.sin(angle)
    canvas.coords(id_planet, x-r, y-r, x+r, y+r)
    angle = angle + 0.1
    canvas.after(50, update_coords, id_planet)

# Initialisation des variables
x = 400
y = 400
r = 30
r_path = 40
angle = 0
ls_planet = []
ls_path = []
angles = [0] * 7  # Liste contenant 7 angles, un pour chaque planète

# creation soleil
id_sun = canvas.create_oval(x-r, y-r, x+r, y+r, fill="orange")

# Création des planetes
for i in range(7):
    r = r + 50
    id_planet = canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue")
    ls_planet.append(id_planet)

# Création trajectoire
for i in range(7):
    x1, y1, x2, y2 = canvas.coords(id_sun)
    canvas.create_oval(x1-r_path, y1-r_path, x2+r_path, y2+r_path)
    ls_path.append(r_path)
    r_path = r_path + 40

# Appel de la fonction de mise à jour toutes les 50 millisecondes
for i in range(7):
    canvas.after(50, update_coords, ls_planet[i], ls_path[i])
print(ls_path)


# Boucle principale de l'application
window.mainloop()