from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

#Conecta al dron y hace que arranque
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

	print("Ready for takooff, taking off...")
	drone.simple_takeoff(TargetAltitude)

	while True:
		Altitude = drone.location.global_relative_frame.alt
		print("altitude: ",Altitude)
		time.sleep(1)

		if Altitude >= TargetAltitude * 0.95:
			print("Altitude reached")
			break


#Vehicle connection (conecci{on con la computadora})
drone = connect('127.0.0.1:14551', wait_ready=True)
arm_and_takeoff(20)
#Coordenadas, altitud y velocidad
drone.airspeed = 10
a_location = LocationGlobalRelative(20.736293,-103.457012,15)
b_location = LocationGlobalRelative(20.736123,-103.457036,15)
c_location = LocationGlobalRelative(20.736167,-103.457287,15)


print("drone en moviendo hacia el primer punto")
drone.simple_goto(a_location)
time.sleep(15)
print("drone en moviendo hacia el segundo punto")
drone.simple_goto(b_location)
time.sleep(15)
print("drone en moviendo hacia el tercer punto")
drone.simple_goto(c_location)
time.sleep(15)
#Regreso al punto inicial
drone.mode = VehicleMode("RTL")
#Muestra la bateria
print(drone.batery.level,"v")