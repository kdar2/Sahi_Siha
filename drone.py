from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil
import json
import math
import time

def load_red_zones(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    

def gorev_ekle(drone):
    komut = drone.commands
    komut.clear()
    
    # WAYPOINT ekle (MAV_CMD_NAV_WAYPOINT_INT kullanıldı)
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.33924753, 149.19886996, 10))
    
    komut.upload()
    print("Komutlar yükleniyor ...")

def main():
    global drone

    print("Drone'a bağlanılıyor...")
    drone = connect('127.0.0.1:14550', wait_ready=True)

    # GUIDED moda geç
    drone.mode = VehicleMode("GUIDED")
    while not drone.is_armable:
        print("Drone arm edilemiyor. Lütfen kontrol edin...")
        time.sleep(1)

    # Arm et
    print("Drone Arm ediliyor")
    drone.armed = True
    while not drone.armed:
        print("Arm edilemedi, tekrar deneniyor...")
        time.sleep(1)
    print("Arm edildi, istenilen irtifaya çıkılıyor")

    # Kalkış yap
    drone.simple_takeoff(10)

    while True:
        print("Mevcut irtifa:", drone.location.global_relative_frame.alt)
        if drone.location.global_relative_frame.alt >= 9.5:
            print("İstenilen irtifaya ulaşıldı.")
            break
        time.sleep(1)

    # Kırmızı bölgeleri belirle
    red_zones = load_red_zones("red_zones.json")
    print(f"HSS alanları: {red_zones}")

    # Görevleri ekle
    gorev_ekle(drone)

    # Kırmızı bölgelerden uzak durmak için ek işlem yapabiliriz.
    # Örneğin, belirli bir alanda uçmayı engellemek için drone hareketlerini kontrol etme vb.

    # İniş yap
    print("İniş yapılıyor...")
    drone.mode = VehicleMode("LAND")
    while drone.location.global_relative_frame.alt > 0:
        print("Mevcut irtifa:", drone.location.global_relative_frame.alt)
        time.sleep(1)
    print("Drone inişi tamamladı.")

    # Bağlantıyı kapat
    drone.close()

if __name__ == "__main__":
    main()
