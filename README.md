# BETA RELEASE v0.5
## Deauthentication Attack Tool
A Python-based deauthentication attack tool designed for Linux terminal use. It automates airmon-ng, airodump-ng, and aireplay-ng to test WiFi security.
# Features
- Works exclusively in Linux terminal.
- Uses Python and Scapy for network packet manipulation.
- Automates Aircrack-ng tools for seamless execution.
- Designed for security testing and educational purposes.
# Installation
### 1. Clone the repository: 
```bash
git clone https://github.com/mertaliasru/Deauthentication_Attack_Tool.git
```
#### Then change directory:
```bash
cd Deauthentication_Attack_Tool
```
### 2. Install Dependecies
```bash
sudo apt update && sudo apt install -y python3 python3-pip aircrack-ng
```
-----------------------------------------
# Usage 
## Ensure you have the necessary permissions:
```bash
chmod +x deauth_tool.py
```
# Running the Tool
## Start the program with root privileges:
```bash
sudo python3 deauth_tool.py
```
------------------------------------------
# ⚙️ How It Works
1️⃣ The tool displays a warning and disclaimer—you must accept to continue.

2️⃣ The program checks if your WiFi adapter supports monitor mode.
- ❌ If unsupported, the tool will exit.
- ✅ If supported, it will automatically enable monitor mode.

3️⃣ The tool scans nearby networks for 30 seconds using airodump-ng.

4️⃣ After scanning, you'll be prompted to select a target network (by SSID).

5️⃣ Choose whether to:
- 🔄 Deauth all devices in the network
- 🎯 Target a specific device based on SSID association.

6️⃣ Select how many deauth packets to send:
- ⚡ 1-999 packets for short interference
- 🚨 1000+ packets for long-term disruption

7️⃣ Once the attack starts:
- 📊 Progress will be displayed
- 🛑 You can stop early using Ctrl+C

8️⃣ When the attack finishes, the tool will ask:
- 🔄 Do you want to perform another attack?
- ✅ Yes: Restart target selection.
- ❌ No: The program will thank you and exit.
-------------------------------------------------------------------------------
# ⚠️ Legal Disclaimer & License
This project is released under the GPL-3.0 License, meaning:
- ✅ Open-source & free to modify.
- ❌ Unauthorized use for illegal activities is strictly prohibited!
- ⚠️ The authors do not take responsibility for any misuse of this tool.

📌 Always ensure you have permission before testing network security. Unauthorized deauthentication attacks may be illegal in your country!
----------------------------------------------------------------------------------------------------------------------------------------------
## 🔗 **Dependencies**
This tool relies on the following security frameworks:
- **Aircrack-ng**: Used for network scanning and deauthentication attacks. [🔗 Website](https://www.aircrack-ng.org/)
- **Linux Terminal & sudo permissions**: Required for proper execution of network commands.



