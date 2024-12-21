from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Drone bağlantısı
drone = connect('127.0.0.1:14550', wait_ready=True)

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

    # Belirtilen irtifaya ulaşana kadar bekle
    while True:
        print(f"Mevcut İrtifa: {drone.location.global_relative_frame.alt:.1f} metre")
        if drone.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Hedef irtifaya ulaşıldı!")
            break
        time.sleep(1)

# Kalkış işlemi
arm_and_takeoff(10)

# Belirtilen konuma git
destination = LocationGlobalRelative(-35.36220671, 149.16507249, 10)
print("Hedef konuma gidiliyor...")
drone.simple_goto(destination)

# Belirtilen konuma ulaşmayı bekle
time.sleep(30)

# İşlemi sonlandır
print("Drone işlemi tamamlandı. LAND moduna geçiliyor...")
drone.mode = VehicleMode("LAND")
while drone.mode != "LAND":
    print("LAND moda geçiliyor...")
    time.sleep(1)
print("Drone iniş yapıyor...")

# Bağlantıyı kapat
drone.close()
