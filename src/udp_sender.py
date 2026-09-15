import socket
import json
import time
from typing import Optional
from src.logger import logger

class UDPSender:
    def __init__(self, target_ip: str = "192.168.50.2", target_port: int = 5005):
        self.target_ip = target_ip
        self.target_port = target_port
        self.socket: Optional[socket.socket] = None
        self.packets_sent: int = 0
        self.last_error_time: float = 0.0

        self.init_socket()

    def init_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Enable broadcast support if needed
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            logger.info(f"UDP Sender initialized. Target: {self.target_ip}:{self.target_port}")
        except Exception as e:
            logger.error(f"Failed to create UDP socket: {e}")
            self.socket = None

    def send_control(self, throttle: int, steering: int) -> bool:
        """
        Sends JSON control packet to ESP32.
        throttle: [-100 .. 100]
        steering: [-100 .. 100]
        """
        if not self.socket:
            self.init_socket()
            if not self.socket:
                return False

        payload = {
            "type": "control",
            "throttle": int(throttle),
            "steering": int(steering),
            "timestamp": int(time.time() * 1000)
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            self.socket.sendto(data, (self.target_ip, self.target_port))
            self.packets_sent += 1
            return True
        except Exception as e:
            now = time.time()
            if now - self.last_error_time > 5.0:  # Prevent spamming error logs
                logger.warning(f"UDP send error to {self.target_ip}:{self.target_port}: {e}")
                self.last_error_time = now
            return False

    def send_emergency_stop(self) -> bool:
        """Sends emergency stop packet (throttle 0, steering 0)."""
        return self.send_control(0, 0)

    def close(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
