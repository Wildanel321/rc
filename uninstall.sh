#!/bin/bash
# ==============================================================================
# Wi-Fi RC Controller Uninstaller Script
# ==============================================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}====================================================${NC}"
echo -e "${YELLOW}    Wi-Fi RC Controller Uninstallation             ${NC}"
echo -e "${YELLOW}====================================================${NC}"

if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Please run uninstaller as root (sudo ./uninstall.sh)${NC}"
  exit 1
fi

echo "[1/4] Stopping rc-controller.service..."
systemctl stop rc-controller.service || true

echo "[2/4] Disabling systemd service..."
systemctl disable rc-controller.service || true
rm -f /etc/systemd/system/rc-controller.service
systemctl daemon-reload

echo "[3/4] Removing application directory (/opt/rc-controller)..."
read -p "Do you want to remove application directory /opt/rc-controller? [y/N] " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    rm -rf /opt/rc-controller
    echo "[OK] Application files removed."
else
    echo "[INFO] Kept application directory /opt/rc-controller."
fi

echo -e "${GREEN}[4/4] Uninstall complete!${NC}"
