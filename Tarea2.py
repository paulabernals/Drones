
#***************************************************************************
# Title        : Assignment2_template.py
#
# Description  : Este archivo es para poder crear un codigo en el cual puedas mover tu dron con 
#                las flechas del teclado. Para este codigo se necesita descargar Tknter.
#
# Environment  : Python 2.7 Code. 
#
# License      : GNU GPL version 3
#
# Editor Used  : Sublime Text
#
#****************************************************************************

#****************************************************************************
# funciones, clases y metodos que tienes que tener importados
#****************************************************************************
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk

#****************************************************************************
#   Method Name     : set_velocity_body
#
#   Description     : Con este comando se envia la velocidad hacia el rumbo que vaya tu dron, 
#                     el eje X, Y, Z se enlazan con el Vehicle.
#                     Eje X: El dron se movera hacia el norte (adelante).
#                     Eje y: El dron se movera hacia el este (derecha).
#                     Eje Z: El dron se movera hacia abajo, pero si es negativo se movera hacia
#                     arriba.
#   Parameters      : vehicle:  vehicle envia el comando
#                     vx: Velocidad X en m/s
#                     vy: Velocidad Y en m/s
#                     vz: Velocidad Z en m/s
#
#   Return Value    : None
#
#   Author           : Paula Xunaxi
#
#****************************************************************************

def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, # BITMASK -> habilita la velocidad.
            0, 0, 0,        #posicion
            vx, vy, vz,     #velocidad
            0, 0, 0,        #aceleracion
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

#****************************************************************************
#   Method Name     : arm_and_takeoff
#
#   Description     : Arma, conecta y arranca el dron.
#
#   Parameters      : targetAltitude
#
#   Return Value    : None
#
#   Author          : Paula Xunaxi
#
#****************************************************************************
def arm_and_takeoff(TargetAltitude):
    print("Executing takeoff")

    while not drone.is_armable:
        print("Vehicle is not armable, waiting....")
        time.sleep(1)

    print("ready to arm")
    drone.mode = VehicleMode("GUIDED")
    drone.armed = True

    while not drone.armed:
        print("Waiting for arming....")
        time.sleep(1)

    print("Ready for takeoff, taking off...")
    drone.simple_takeoff(TargetAltitude)

    while True:
        Altitude = drone.location.global_relative_frame.alt
        print("altitude:",Altitude)
        time.sleep(1)

        if Altitude >= TargetAltitude * 0.95:
            print("Altitude reached")
            break


#****************************************************************************
#   Method Name     : key
#
#   Description     : Con este comando, se asignan las velocidades y se enlaza con Tkinter para
#                     que se ejecute las claves que se quiere.
#
#   Parameters      : tkinter, conecta el teclado con las claves, haciendo que el dron vaya a una
#                     direccion especifica.
#
#   Return Value    : None
#
#   Author          : Paula Xunaxi
#
#****************************************************************************
def key(event):
    if event.char == event.keysym: #inician las claves
        if event.keysym == 'r':
            drone.mode = VehicleMode("RTL")

    #Codigo que se ejecuta        
    else: #claves
    #Para que el dron vaya hacia arriba use el siguiente comando
        if event.keysym == 'Up':
            set_velocity_body(drone,5,0,0)
    #Para que el dron vaya hacia abajo use el siguiente comando
        elif event.keysym == 'Down':
            set_velocity_body(drone,-5,0,0)
    #Para que el dron vaya hacia la izquierda use el siguiente comando
        elif event.keysym == 'Left':
            set_velocity_body(drone,0,-5,0)
    #Para que el dron vaya hacia la derecha use el siguiente comando
        elif event.keysym == 'Right':
            set_velocity_body(drone,0,5,0)

#****************************************************************************
#   Codigos principales
#
#****************************************************************************

# codigo para conectar con el dron #
drone = connect('127.0.0.1:14551', wait_ready=True)

# El dron despega a 10 m de altitud
arm_and_takeoff(10)
 
# Con el siguiente codigo Tkinter se conecta con el teclado, para que al presionar cualquier flecha del teclado, 
# llame a la clave correspondiente, haciendo que el dron vaya a la direccion que se quiere.
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()