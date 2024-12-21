from dronekit import connect, VehicleMode, LocationGlobalRelative ,Command
from pymavlink.dialects.v20 import common as mavlink
from pymavlink import mavutil
import time

drone = connect('127.0.0.1:14550',wait_ready=True)


def arm_and_takeoff(target_altitude):
    """
    Drone'u GUIDED moda al, ARM et ve belirtilen irtifaya yüksel.
    """
    print("Pre-arm checks yapılıyor...")
    # Drone arm edilebilir durumda olmasını bekle
    while not drone.is_armable:
        print("Drone arm edilebilir durumda değil, bekleniyor...")
        time.sleep(1)
    
    print("Drone arm edilebilir. Mod GUIDED'e alınıyor.")
    drone.mode = VehicleMode("GUIDED")
    while drone.mode != "GUIDED":
        print("GUIDED moda geçiliyor...")
        time.sleep(1)

    # Drone'u arm et
    print("Drone arm ediliyor...")
    drone.armed = True
    while not drone.armed:
        print("Drone arm ediliyor, bekleniyor...")
        time.sleep(1)
    print("Drone arm edildi!")

    # Kalkış işlemi
    print(f"{target_altitude} metreye kalkış yapılıyor...")
    drone.simple_takeoff(target_altitude)

    while True:
        print(f"Mevcut İrtifa: {drone.location.global_relative_frame.alt:.1f} metre")
        if drone.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Hedef irtifaya ulaşıldı!")
            break
        time.sleep(1)

arm_and_takeoff(10)


def gorev_ekle():
    global komut
    komut = drone.commands

    komut.clear()
    print(drone.battery)
    #TAKEOFF komudu
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,0,0,0,0,0,0,0,10))

    #WAYPOINT komudu
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,-35.36194845 ,149.16772988, 10))
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,-35.36312616 ,149.16741755, 10))
    # komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,-35.36081233 , 149.16356473 , 10))

    # komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0, -35.36261713 ,149.16455484  , 10))


    #RTL komudu
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0))
   
    #DOĞRULAMA 
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0))

    komut.upload()
    
    print("komutlar yükleniyor...")
    
    
gorev_ekle()
    
komut.next = 0
    
drone.mode = VehicleMode("AUTO")
    
while True:
    next_waypoint = komut.next
    
    print(f"sıradaki komut{next_waypoint}")
    
    if next_waypoint is 4 :
        print("Görev bitti.")
        break
    print("döngüden çıktı.")
    time.sleep(1.5)