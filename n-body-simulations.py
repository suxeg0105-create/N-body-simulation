import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import random 
from math import acos, sin

G = 6.67 * 10 ** (-11) 
N = 500
dt = 0.01

def r(x1, y1, x2, y2):
    return  ((x1 - x2) ** 2 + (y1 - y2) ** 2 + 0.1 ) ** 0.5

def punch(o_1, o_2):
    v_1 = (o_1[3] ** 2 + o_1[4] ** 2) ** 0.5
    v_2 = (o_2[3] ** 2 + o_2[4] ** 2) ** 0.5

    cos_b = (o_1[1] - o_2[1]) / r(o_1[1], o_1[2], o_2[1], o_2[2])
    sin_b = (o_1[2] - o_2[2]) / r(o_1[1], o_1[2], o_2[1], o_2[2])

    cos_a = (cos_b * o_1[3] + sin_b * o_1[4]) / v_1
    sin_a = sin(acos(cos_a))

    cos_y = -(cos_b * o_2[3] + sin_b * o_2[4]) / v_2
    sin_y = sin(acos(cos_y))

    v_new_x_1 = ((o_1[0] - o_2[0]) * v_1 * cos_a + 2 * o_2[0] * v_2 * cos_y)/ (o_1[0] + o_2[0])
    v_new_x_2 = ((o_2[0] - o_1[0]) * v_2 * cos_y + 2 * o_1[0] * v_1 * cos_a)/ (o_1[0] + o_2[0])

    v_new_y_1 = v_1 * sin_a
    v_new_y_2 = v_2 * sin_y

    v_x_1 = v_new_x_1 * cos_b + v_new_y_1 * sin_b
    v_y_1 = v_new_x_1 * sin_b - v_new_y_1 * cos_b

    v_x_2 = v_new_x_2 * cos_b + v_new_y_2 * sin_b
    v_y_2 = v_new_x_2 * sin_b - v_new_y_2 * cos_b

    return [[v_x_1, v_y_1 ], [v_x_2, v_y_2]]
   



    


# info_planet = [mass, x, y, v_x, v_y]

def a_conculation(system):
    a_answear = []
    for i in range(N):
        a_answear.append([0.0, 0.0])


    for i in range(len(system)):
        for j in range(len(system)):
            if i == j:
                continue
            else:
                mass_factor = -G * system[j][0] / (r(system[j][1], system[j][2], system[i][1], system[i][2])) ** 3
                a_x = (system[i][1] - system[j][1]) * mass_factor
                a_y = (system[i][2] - system[j][2]) * mass_factor 
                a_answear[i][0] += a_x
                a_answear[i][1] += a_y

    return a_answear

system = []

for i in range(N):
    planet_1 = [10, random.uniform(1.0, 10), random.uniform(1.0, 10), random.uniform(1.0, 10), random.uniform(1.0, 10)]
    system.append(planet_1)



fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 15)
ax.set_ylim(0, 15)
ax.grid(False)


dots = []
for i in range(len(system)):
    dot = ax.scatter(system[i][1], system[i][2], s=50, color="blue")
    dots.append(dot)


a = a_conculation(system)
E = []

def update(frame):
    global dots, system, a, E

    
    for i in range(N):
        system[i][3] += 0.5 * (a[i][0] ) * dt 
        system[i][4] += 0.5 * (a[i][1] ) * dt

    for i in range(N):
        system[i][1] += 2 * system[i][3] * dt + 0.5 * a[i][0] * dt ** 2
        system[i][2] += 2 * system[i][4] * dt + 0.5 * a[i][1] * dt ** 2

    for i in range(N):
        for j in range(i + 1, N):
            if i == j:
                continue 
            if r(system[i][1], system[i][2], system[j][1], system[j][2]) <= 0.1:
                new = punch(system[i], system[j])
                system[i][3] = new[0][0]
                system[i][4] = new[0][1]

                system[j][3] = new[1][0]
                system[j][4] = new[1][1]
   

    x_min, x_max = 0, 15
    y_min, y_max = 0, 15
    coef = 1.0           # 1.0 — абсолютно упругий, можно 0.9 для потери энергии

    for i in range(N):
    # По X
        if system[i][1] < x_min:
            system[i][1] = x_min
            system[i][3] = -coef * system[i][3]   # vx
        elif system[i][1] > x_max:
            system[i][1] = x_max
            system[i][3] = -coef * system[i][3]
    # По Y
        if system[i][2] < y_min:
            system[i][2] = y_min
            system[i][4] = -coef * system[i][4]   # vy
        elif system[i][2] > y_max:
            system[i][2] = y_max
            system[i][4] = -coef * system[i][4]
    a_new = a_conculation(system)

    for i in range(N):
        dots[i].set_offsets([system[i][1], system[i][2]])

    for i in range(N):
        system[i][3] += 0.25 * (a[i][0] + a_new[i][0]) * dt 
        system[i][4] += 0.25 * (a[i][1] + a_new[i][1]) * dt

    E_all = 0.0
    for i in range(N):
        E_all +=  system[i][0] * (system[i][3] ** 2 + system[i][4] ** 2)  * 0.5 
    
    for i in range(N):
        for j in range(i + 1, N):
            E_all += - system[i][0] * system[j][0] * G / r(system[i][1], system[i][2], system[j][1], system[j][2])
            
    E.append(E_all  ) 

    a = a_new


    

    return dots


ani = FuncAnimation(fig, update, frames=None, interval=20, blit=True)
plt.show()


fig_1 , ax_1 = plt.subplots(figsize=(10,10))
ax_1.set_ylim(min(E)/ 1, max(E) * 1.)
ax_1.plot(E)
plt.show()               


