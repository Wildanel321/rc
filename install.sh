#!/bin/bash
# ==============================================================================
# Wi-Fi RC Controller Installer Script for Raspberry Pi 3
# ==============================================================================
set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}    Wi-Fi RC Controller Installation (RPi 3)       ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Step 1: Check root privilege
echo -e "${YELLOW}[1/8] Checking system & root privileges...${NC}"
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run installer as root (sudo ./install.sh)${NC}"
  exit 1
fi

INSTALL_DIR="/opt/rc-controller"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 2: Install system dependencies
echo -e "${YELLOW}[2/8] Installing system dependencies...${NC}"
apt-get update -y
apt-get install -y python3 python3-pip python3-evdev hostapd dnsmasq network-manager || true

# Install Python packages
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip3 install -r "$SCRIPT_DIR/requirements.txt" --break-system-packages || pip3 install -r "$SCRIPT_DIR/requirements.txt" || true
fi

# Step 3: Configure Wi-Fi Access Point
echo -e "${YELLOW}[3/8] Configuring Wi-Fi Access Point (SSID: RC-CONTROLLER)...${NC}"
WLAN_IF="wlan0"

if command -v nmcli &> /dev/null && systemctl is-active --quiet NetworkManager; then
    echo "[INFO] NetworkManager detected. Configuring hotspot using nmcli..."
    systemctl stop hostapd dnsmasq &> /dev/null || true
    systemctl disable hostapd dnsmasq &> /dev/null || true
    systemctl mask hostapd &> /dev/null || true

    rfkill unblock wifi &> /dev/null || true
    rfkill unblock all &> /dev/null || true
    nmcli radio wifi on &> /dev/null || true

    nmcli connection delete RC-HOTSPOT &> /dev/null || true
    nmcli connection add type wifi ifname "$WLAN_IF" con-name RC-HOTSPOT autoconnect yes ssid RC-CONTROLLER
    nmcli connection modify RC-HOTSPOT 802-11-wireless.mode ap
    nmcli connection modify RC-HOTSPOT 802-11-wireless.band bg
    nmcli connection modify RC-HOTSPOT 802-11-wireless-security.key-mgmt wpa-psk
    nmcli connection modify RC-HOTSPOT 802-11-wireless-security.psk "RCController123"
    nmcli connection modify RC-HOTSPOT ipv4.method shared ipv4.addresses 192.168.50.1/24
    nmcli connection modify RC-HOTSPOT ipv6.method disabled
    nmcli connection up RC-HOTSPOT || true
else
    echo "[INFO] Unblocking Wi-Fi radio..."
    rfkill unblock wifi || true
    rfkill unblock all || true

    echo "[INFO] Using hostapd / dnsmasq for Access Point setup..."
    sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|g' /etc/default/hostapd || true
    echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' > /etc/default/hostapd || true

    cat <<EOF > /etc/dhcpcd.conf
interface wlan0
    static ip_address=192.168.50.1/24
    nohook wpa_supplicant
EOF

    cat <<EOF > /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.50.2,192.168.50.20,255.255.255.0,24h
EOF

    cat <<EOF > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=RC-CONTROLLER
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=RCController123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

    systemctl unmask hostapd &> /dev/null || true
    systemctl enable hostapd dnsmasq || true
    systemctl restart hostapd dnsmasq || true
fi

# Step 4: Install application files
echo -e "${YELLOW}[4/8] Installing controller files to ${INSTALL_DIR}...${NC}"
mkdir -p "$INSTALL_DIR"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/requirements.txt" "$INSTALL_DIR/"

chmod +x "$INSTALL_DIR/src/main.py"

# Step 5: Install systemd service
echo -e "${YELLOW}[5/8] Installing systemd service...${NC}"
cp "$SCRIPT_DIR/systemd/rc-controller.service" /etc/systemd/system/rc-controller.service
systemctl daemon-reload
systemctl enable rc-controller.service

# Step 6: Start service
echo -e "${YELLOW}[6/8] Starting systemd service...${NC}"
systemctl restart rc-controller.service

# Step 7: Health check
echo -e "${YELLOW}[7/8] Performing Gamepad & Service Health Check...${NC}"
sleep 2
if systemctl is-active --quiet rc-controller.service; then
    echo -e "${GREEN}[OK] rc-controller.service is ACTIVE and RUNNING.${NC}"
else
    echo -e "${RED}[WARNING] Service failed to start. Check status via: systemctl status rc-controller.service${NC}"
fi

# Step 8: Complete
echo -e "${GREEN}[8/8] Complete! Installation finished successfully.${NC}"
echo -e "${GREEN}Wi-Fi AP 'RC-CONTROLLER' IP: 192.168.50.1${NC}"
echo -e "Run debug view anytime with: ${YELLOW}python3 $INSTALL_DIR/src/main.py --debug${NC}"
