import math
import json

# Kırmızı alanları tutacak bir liste
red_zones = []

def save_red_zones_to_file():
    """Kırmızı alanları bir dosyaya kaydet."""
    with open("red_zones.json", "w") as file:
        json.dump(red_zones, file)
    print("Kırmızı alanlar 'red_zones.json' dosyasına kaydedildi.")

def load_red_zones_from_file():
    """Kırmızı alanları bir dosyadan yükle."""
    global red_zones
    try:
        with open("red_zones.json", "r") as file:
            red_zones = json.load(file)
        print("Kırmızı alanlar 'red_zones.json' dosyasından yüklendi.")
    except FileNotFoundError:
        print("'red_zones.json' dosyası bulunamadı. Yeni bir liste oluşturulacak.")

def add_red_zone():
    """Kırmızı alan tanımlama fonksiyonu."""
    enlem = float(input("Kırmızı alan merkezinin enlemini girin (örn. 40.23351019): "))
    boylam = float(input("Kırmızı alan merkezinin boylamını girin (örn. 28.99976492): "))
    yaricap = float(input("Kırmızı alan yarıçapını girin (metre cinsinden, örn. 50): "))
    red_zones.append({"center": (enlem, boylam), "radius": yaricap})
    print(f"Kırmızı alan eklendi: Merkez=({enlem}, {boylam}), Yarıçap={yaricap} metre")
    save_red_zones_to_file()  # Her eklemeden sonra dosyaya kaydedilir.

def is_in_red_zone(drone_position):
    """Drone'un kırmızı alan içinde olup olmadığını kontrol eder."""
    for zone in red_zones:
        # Kırmızı alan merkezi ve yarıçap
        zone_center = zone["center"]
        zone_radius = zone["radius"]
        
        # Enlem-boylam farkını metreye çevirmek için basit bir düz hesap (küçük alanlar için yeterlidir)
        delta_lat = (drone_position[0] - zone_center[0]) * 111000  # Enlem farkı metreye
        delta_lon = (drone_position[1] - zone_center[1]) * 111000 * math.cos(math.radians(zone_center[0]))  # Boylam farkı metreye
        
        # İki nokta arasındaki mesafeyi hesapla
        distance = math.sqrt(delta_lat**2 + delta_lon**2)
        
        if distance < zone_radius:
            return True  # Kırmızı alan içinde
    return False  # Kırmızı alan dışında

def main():
    """Ana kontrol akışı."""
    load_red_zones_from_file()  # Program başlarken kırmızı alanları yükle.
    print("Kırmızı alan tanımlama ve kontrol sistemi.")
    
    while True:
        print("\n1. Yeni bir kırmızı alan ekle")
        print("2. Drone konumunu kontrol et")
        print("3. Çıkış")
        choice = input("Seçiminizi yapın: ")
        
        if choice == "1":
            add_red_zone()
        elif choice == "2":
            drone_lat = float(input("Drone'un enlemini girin: "))
            drone_lon = float(input("Drone'un boylamını girin: "))
            if is_in_red_zone((drone_lat, drone_lon)):
                print("Drone kırmızı alan içinde! Uçuş yasak.")
            else:
                print("Drone güvenli alanda.")
        elif choice == "3":
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
