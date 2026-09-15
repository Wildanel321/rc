import sys
import time
import argparse
import os
from pathlib import Path

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import ConfigManager

from src.logger import logger
from src.gamepad import GamepadReader
from src.input_mapper import InputMapper
from src.safety import SafetyController, SafetyState
from src.udp_sender import UDPSender

def clear_screen():
    # Clear console screen for status dashboard
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard(
    ap_status: str,
    gamepad_status: str,
    target_addr: str,
    throttle: int,
    steering: int,
    left_motor: int,
    right_motor: int,
    rate_hz: int,
    safety_str: str,
    packets_sent: int
):
    clear_screen()
    print("==================================================")
    print("           Wi-Fi RC CONTROLLER (RPi 3)            ")
    print("==================================================")
    print(f" Wi-Fi AP  : {ap_status}")
    print(f" Gamepad   : {gamepad_status}")
    print(f" ESP32 UDP : {target_addr}")
    print("--------------------------------------------------")
    print(f" Throttle  : {throttle:+4d}%  |  Steering : {steering:+4d}%")
    print(f" Motor L   : {left_motor:+4d}%  |  Motor R  : {right_motor:+4d}%")
    print("--------------------------------------------------")
    print(f" Rate      : {rate_hz} Hz")
    print(f" Safety    : {safety_str}")
    print(f" UDP Sent  : {packets_sent} packets")
    print("==================================================")
    print(" Press Ctrl+C to exit cleanly.")

def main():
    parser = argparse.ArgumentParser(description="Wi-Fi RC Controller (Raspberry Pi 3)")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug stream")
    parser.add_argument("--test", action="store_true", help="Run in test simulation mode without physical sending")
    parser.add_argument("--config", type=str, default=None, help="Custom configuration JSON path")
    args = parser.parse_args()

    # Load Configuration
    config_mgr = ConfigManager(args.config)
    net_cfg = config_mgr.network
    ctrl_cfg = config_mgr.controller
    safe_cfg = config_mgr.safety

    # Initialize Modules
    input_mapper = InputMapper(
        deadzone=ctrl_cfg.get("deadzone", 0.10),
        invert_throttle=ctrl_cfg.get("invert_throttle", True),
        invert_steering=ctrl_cfg.get("invert_steering", False),
        max_speed=ctrl_cfg.get("max_speed", 100),
        acceleration_step=ctrl_cfg.get("acceleration_step", 10.0)
    )

    safety = SafetyController()
    udp_sender = UDPSender(
        target_ip=net_cfg.get("esp32_ip", "192.168.50.2"),
        target_port=net_cfg.get("udp_port", 5005)
    )

    gamepad = GamepadReader(
        on_disconnect=safety.on_gamepad_disconnect,
        on_reconnect=lambda name: safety.reset_emergency_stop(),
        emergency_buttons=safe_cfg.get("emergency_buttons", ["BTN_START", "BTN_SELECT"])
    )

    # Initial Connection Attempt
    gamepad.connect()
    gamepad.start_listening()

    packet_rate = net_cfg.get("packet_rate", 50)
    loop_interval = 1.0 / packet_rate

    logger.info(f"Starting main control loop at {packet_rate} Hz (interval {loop_interval*1000:.1f} ms)...")

    dashboard_timer = 0
    try:
        while True:
            start_time = time.time()

            # Read raw stick values (-1.0 to 1.0)
            raw_x, raw_y = gamepad.get_axes()

            # Check Gamepad Emergency Button Trigger
            if gamepad.emergency_stop_triggered:
                safety.trigger_emergency_stop("Gamepad Emergency Button")
                gamepad.emergency_stop_triggered = False

            # Calculate Motor Outputs
            if safety.is_safe() and gamepad.is_connected:
                # Calculate differential drive & ramped acceleration
                target_left, target_right = input_mapper.compute_differential_drive(raw_x, raw_y)
                left_motor, right_motor = input_mapper.update_smooth_acceleration(target_left, target_right)
                
                # Derive overall throttle & steering for telemetry
                throttle = (left_motor + right_motor) // 2
                steering = (left_motor - right_motor) // 2
            else:
                # Unsafe state (emergency stop or gamepad disconnected) -> Force Motors STOP
                input_mapper.reset_smooth_acceleration()
                left_motor, right_motor = 0, 0
                throttle, steering = 0, 0

            # Transmit UDP Packet (Unless in test mode)
            if not args.test:
                udp_sender.send_control(left_motor, right_motor)

            # Debug Telemetry Stream
            if args.debug:
                gamepad_str = gamepad.device_name if gamepad.is_connected else "DISCONNECTED"
                print(
                    f"[DEBUG] RAW: X={raw_x:+.2f} Y={raw_y:+.2f} | "
                    f"MOTOR: L={left_motor:+4d} R={right_motor:+4d} | "
                    f"STAT: {gamepad_str} | SAFETY: {safety.get_status_str()} | "
                    f"UDP: {udp_sender.packets_sent}"
                )
            else:
                # Dashboard view update every ~100ms
                dashboard_timer += 1
                if dashboard_timer >= (packet_rate // 10 or 1):
                    dashboard_timer = 0
                    gamepad_str = f"CONNECTED ({gamepad.device_name})" if gamepad.is_connected else "DISCONNECTED"
                    render_dashboard(
                        ap_status="READY",
                        gamepad_status=gamepad_str,
                        target_addr=f"{udp_sender.target_ip}:{udp_sender.target_port}",
                        throttle=int(throttle),
                        steering=int(steering),
                        left_motor=int(left_motor),
                        right_motor=int(right_motor),
                        rate_hz=packet_rate,
                        safety_str=safety.get_status_str(),
                        packets_sent=udp_sender.packets_sent if not args.test else 0
                    )

            # Enforce fixed control loop rate
            elapsed = time.time() - start_time
            sleep_time = loop_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("\nShutting down controller...")
    finally:
        # Emergency stop on exit
        udp_sender.send_emergency_stop()
        gamepad.stop_listening()
        udp_sender.close()
        logger.info("Controller stopped cleanly.")

if __name__ == "__main__":
    main()
