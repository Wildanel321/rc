# Wi-Fi RC Controller (Raspberry Pi 3 + ESP32 + L298N)

A high-performance, low-latency wireless Remote Control (RC) system using **Raspberry Pi 3** as a standalone Wi-Fi Access Point & USB Gamepad Controller and **ESP32** as an onboard motor receiver driving an **L298N dual motor driver**.

> **Zero Internet / Router Dependency**: The Raspberry Pi generates its own Wi-Fi Access Point. The system operates completely offline with active real-time safety watchdog protection.

---

## 1. System Architecture

```text
                 USB
          ┌──────────────┐
          │ USB GAMEPAD  │
          └──────┬───────┘
                 │
                 ▼
       ┌───────────────────┐
       │   RASPBERRY PI 3  │
       │                   │
       │ Gamepad Reader    │
       │ Input Processing  │
       │ UDP Sender        │
       │ Wi-Fi Access Point│
       └─────────┬─────────┘
                 │
              Wi-Fi (SSID: RC-CONTROLLER)
                 │
              UDP :5005 (50 Hz)
                 │
                 ▼
       ┌───────────────────┐
       │       ESP32       │
       │                   │
       │ UDP Receiver      │
       │ Active Watchdog   │
       │ Motor Controller  │
       └─────────┬─────────┘
                 │
                 ▼
              L298N
              /    \
             /      \
        Motor L    Motor R
```

---

## 2. Hardware Requirements & Wiring

### Controller Side
- **Raspberry Pi 3** (running Raspberry Pi OS)
- **USB Gamepad** (Generic / Xbox / PlayStation controller)

### RC Vehicle Side
- **ESP32 DevKit V1**
- **L298N Dual H-Bridge Motor Driver**
- **2 DC Motors** (Differential / Tank drive)
- **Battery Pack** (7.4V - 12V LiPo/LiFePO4 for motors, 5V regulator for ESP32/L298N logic)

### Default GPIO Mapping (`esp32/rc_receiver/config.h`)

| L298N Pin | ESP32 GPIO Pin | Description |
|-----------|----------------|-------------|
| **ENA** (spedA) | GPIO 25 | Left Motor PWM Speed Control |
| **IN1** (en1)   | GPIO 13 | Left Motor Direction 1 |
| **IN2** (en2)   | GPIO 12 | Left Motor Direction 2 |
| **ENB** (spedB) | GPIO 26 | Right Motor PWM Speed Control |
| **IN3** (en3)   | GPIO 14 | Right Motor Direction 1 |
| **IN4** (en4)   | GPIO 27 | Right Motor Direction 2 |


> **IMPORTANT**: Remove the jumpers from ENA and ENB on the L298N board so that the ESP32 can send PWM signals directly to controls motor speed.

---

## 3. Installation Guide (Raspberry Pi 3)

### Automated Installation

Clone this repository to your Raspberry Pi and execute the installer:

```bash
git clone https://github.com/your-user/rc.git
cd rc
sudo ./install.sh
```

The installer automatically performs 8 setup phases:
1. Validates system requirements and root privileges.
2. Installs required packages (`python3-evdev`, `hostapd`, `dnsmasq`, `network-manager`).
3. Sets up Wi-Fi AP (`SSID: RC-CONTROLLER`, `IP: 192.168.50.1`).
4. Installs controller application files to `/opt/rc-controller`.
5. Registers systemd service `rc-controller.service`.
6. Starts background controller service.
7. Conducts health check on USB gamepad.
8. Displays completion summary.

---

## 4. ESP32 Firmware Setup

1. Open `esp32/rc_receiver/rc_receiver.ino` in **Arduino IDE** or **PlatformIO**.
2. Install **ArduinoJson** library (`v6.x` or `v7.x`).
3. Verify Wi-Fi SSID, Password, and GPIO pins in `esp32/rc_receiver/config.h`:
   ```cpp
   #define WIFI_SSID     "RC-CONTROLLER"
   #define WIFI_PASSWORD "RCController123"
   #define UDP_PORT      5005
   ```
4. Select **ESP32 Dev Module** board and flash the firmware.
5. Open Serial Monitor at **115200 baud**. You should see:
   ```text
   [WiFi] Connecting...
   [WiFi] Connected
   [WiFi] IP: 192.168.50.2
   [UDP] Listening on port 5005
   [RC] READY
   ```

---

## 5. Usage & Command-Line Modes

### Service Status
Check the status of the background service:
```bash
sudo systemctl status rc-controller.service
```

### CLI Status Dashboard (Interactive View)
```bash
python3 /opt/rc-controller/src/main.py
```

### Live Debug Stream
```bash
python3 /opt/rc-controller/src/main.py --debug
```
Output:
```text
[DEBUG] RAW: X=+0.52 Y=-0.84 | MOTOR: L=+100 R=+32 | STAT: Generic USB Gamepad | SAFETY: ARMED | UDP: 1245
```

### Simulation / Test Mode (Without Hardware)
```bash
python3 /opt/rc-controller/src/main.py --test
```

### Interactive Serial Motor Test (ESP32)
Connect the ESP32 to USB and send text commands via Serial Monitor:
- `forward 50`
- `reverse 30`
- `left 50`
- `right 50`
- `stop`

---

## 6. Configuration (`config/controller.json`)

```json
{
    "network": {
        "esp32_ip": "192.168.50.2",
        "udp_port": 5005,
        "packet_rate": 50
    },
    "controller": {
        "deadzone": 0.10,
        "invert_throttle": true,
        "invert_steering": false,
        "max_speed": 100,
        "acceleration_step": 10
    },
    "safety": {
        "failsafe_ms": 300,
        "emergency_buttons": ["BTN_START", "BTN_SELECT"]
    }
}
```

---

## 7. UDP Control Protocol

- **Transport**: UDP
- **Port**: 5005
- **Rate**: 50 Hz (20 ms interval)
- **JSON Payload Format**:
  ```json
  {
      "type": "control",
      "throttle": 80,
      "steering": -20,
      "timestamp": 1694572800000
  }
  ```

---

## 8. Safety & Active Failsafe Rules

1. **Default Stop**: Motors are set to `0` output upon boot.
2. **ESP32 Active Watchdog**: If no valid UDP packet is received for **>300 ms**, ESP32 immediately halts all motors (`EMERGENCY STOP`).
3. **Gamepad Disconnect Handling**: If the USB Gamepad is unplugged, Raspberry Pi sends an emergency stop packet instantly and stops sending control packets.
4. **Emergency Stop Buttons**: Pressing `START` or `SELECT` on the gamepad immediately zero-loads all outputs until manually reset.
5. **Wi-Fi Disconnect**: If Wi-Fi link drops, ESP32 stops motors immediately and enters reconnect loop.

---

## 9. Testing Plan (10 Test Phases)

1. **TEST 1 — Gamepad**: Verify USB Gamepad detection with `evdev`.
2. **TEST 2 — Input Mapping**: Verify left stick Y (throttle) and X (steering) mapping.
3. **TEST 3 — Wi-Fi AP**: Confirm `RC-CONTROLLER` SSID appears on nearby Wi-Fi scans.
4. **TEST 4 — ESP32 Connection**: Verify ESP32 connects to `RC-CONTROLLER` AP and receives IP `192.168.50.x`.
5. **TEST 5 — UDP Packet Flow**: Test packet transmission using `main.py --debug`.
6. **TEST 6 — Serial Command Test**: Use Serial Monitor `forward 50` to verify L298N wiring.
7. **TEST 7 — End-to-End Control**: Test vehicle movement with wheels elevated.
8. **TEST 8 — Failsafe Verification**: Disconnect Pi; verify ESP32 stops motors within 300 ms.
9. **TEST 9 — Wi-Fi Loss**: Turn off Pi AP; verify ESP32 immediately halts motors.
10. **TEST 10 — Gamepad Unplug**: Disconnect USB Gamepad; verify Pi sends stop command.

---

## 10. Troubleshooting Guide

| Issue | Root Cause | Solution |
|-------|------------|----------|
| **Gamepad not detected** | USB permissions or unsupported input event | Ensure user has input group permissions (`sudo usermod -aG input $USER`) and `evdev` is installed. |
| **Wi-Fi AP not appearing** | `wlan0` blocked or hostapd service down | Run `sudo rfkill unblock wlan` and `sudo systemctl status hostapd`. |
| **ESP32 won't connect** | Wrong SSID or Password | Verify credentials in `esp32/rc_receiver/config.h`. |
| **Motors spinning opposite direction** | Inverted motor wiring | Swap motor terminals on L298N block or adjust `invert_throttle`/`invert_steering` in `config/controller.json`. |
| **Motors stuttering** | Low battery voltage | Check LiPo/battery supply under load. |
| **Failsafe triggering continuously** | High packet loss or wrong IP | Verify target `esp32_ip` in `config/controller.json` matches ESP32 local IP. |

---

## 11. Uninstallation

To remove the controller service and files:

```bash
sudo ./uninstall.sh
```

---

## 12. License

This project is licensed under the [MIT License](LICENSE).
