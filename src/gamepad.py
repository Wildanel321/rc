import time
import threading
from typing import Callable, Optional, Dict, Any
from src.logger import logger

try:
    import evdev
    from evdev import InputDevice, list_devices, ecodes
    EVDEV_AVAILABLE = True
except ImportError:
    EVDEV_AVAILABLE = False
    evdev = None

class GamepadReader:
    def __init__(
        self,
        on_disconnect: Optional[Callable[[], None]] = None,
        on_reconnect: Optional[Callable[[str], None]] = None,
        emergency_buttons: list = None
    ):
        self.on_disconnect = on_disconnect
        self.on_reconnect = on_reconnect
        self.emergency_buttons = emergency_buttons or ["BTN_START", "BTN_SELECT"]

        self.device: Optional[Any] = None
        self.device_name: str = "Unknown Gamepad"
        self.is_connected: bool = False
        self.running: bool = False

        # Current axis normalized state (-1.0 to 1.0)
        self.axis_x: float = 0.0
        self.axis_y: float = 0.0

        # Axis min/max bounds for normalization
        self.abs_x_min = -32768
        self.abs_x_max = 32767
        self.abs_y_min = -32768
        self.abs_y_max = 32767

        # Buttons state
        self.emergency_stop_triggered: bool = False

        self._thread: Optional[threading.Thread] = None

    @staticmethod
    def find_gamepad() -> Optional[Any]:
        """Scans /dev/input/event* for gamepads."""
        if not EVDEV_AVAILABLE:
            return None

        devices = [InputDevice(path) for path in list_devices()]
        for dev in devices:
            capabilities = dev.capabilities()
            # Check if device has EV_ABS (joystick/axes) and EV_KEY (buttons)
            if ecodes.EV_ABS in capabilities and ecodes.EV_KEY in capabilities:
                # Basic check to exclude keyboards or power buttons
                keys = capabilities[ecodes.EV_KEY]
                # Gamepads usually have BTN_GAMEPAD, BTN_SOUTH, BTN_A, or BTN_TRIGGER
                gamepad_keys = {
                    ecodes.BTN_GAMEPAD, ecodes.BTN_SOUTH, ecodes.BTN_A,
                    ecodes.BTN_TRIGGER, ecodes.BTN_START, ecodes.BTN_SELECT,
                    ecodes.BTN_MODE, ecodes.BTN_TL, ecodes.BTN_TR
                }
                if any(k in keys for k in gamepad_keys):
                    return dev
        return None

    def connect(self) -> bool:
        """Attempts to find and connect to a gamepad."""

        logger.info("Searching for gamepad...")
        if not EVDEV_AVAILABLE:
            logger.warning("evdev library unavailable (non-Linux OS). Using mock/manual mode.")
            return False

        dev = self.find_gamepad()
        if dev:
            self.device = dev
            self.device_name = dev.name
            self.is_connected = True
            
            # Read ABS info for scaling
            abs_info = dev.absinfo(ecodes.ABS_X) if ecodes.ABS_X in dev.capabilities().get(ecodes.EV_ABS, {}) else None
            if abs_info:
                self.abs_x_min = abs_info.min
                self.abs_x_max = abs_info.max

            abs_info_y = dev.absinfo(ecodes.ABS_Y) if ecodes.ABS_Y in dev.capabilities().get(ecodes.EV_ABS, {}) else None
            if abs_info_y:
                self.abs_y_min = abs_info_y.min
                self.abs_y_max = abs_info_y.max

            logger.info(f"Gamepad detected: {self.device_name}")
            logger.info("Controller ready")
            if self.on_reconnect:
                self.on_reconnect(self.device_name)
            return True
        else:
            logger.warning("No USB Gamepad found.")
            return False

    def start_listening(self):
        """Starts background reader thread."""
        self.running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop_listening(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

    def _normalize_axis(self, val: int, val_min: int, val_max: int) -> float:
        center = (val_max + val_min) / 2.0
        half_range = (val_max - val_min) / 2.0
        if half_range == 0:
            return 0.0
        norm = (val - center) / half_range
        return max(-1.0, min(1.0, norm))

    def _read_loop(self):
        while self.running:
            if not self.is_connected:
                # Auto-reconnect loop
                time.sleep(1.0)
                if self.connect():
                    continue
                else:
                    continue

            try:
                for event in self.device.read_loop():
                    if not self.running:
                        break

                    # Handle Axis Motion
                    if event.type == ecodes.EV_ABS:
                        if event.code == ecodes.ABS_X:
                            self.axis_x = self._normalize_axis(event.value, self.abs_x_min, self.abs_x_max)
                        elif event.code == ecodes.ABS_Y:
                            self.axis_y = self._normalize_axis(event.value, self.abs_y_min, self.abs_y_max)

                    # Handle Buttons
                    elif event.type == ecodes.EV_KEY:
                        key_name = ecodes.KEY.get(event.code, ecodes.BTN.get(event.code, ""))
                        # Key pressed down (value 1)
                        if event.value == 1:
                            if isinstance(key_name, list):
                                is_e_btn = any(b in self.emergency_buttons for b in key_name)
                            else:
                                is_e_btn = key_name in self.emergency_buttons

                            if is_e_btn:
                                logger.critical(f"Emergency stop button pressed! ({key_name})")
                                self.emergency_stop_triggered = True

            except (OSError, IOError) as e:
                logger.warning("Gamepad disconnected")
                logger.warning("Sending emergency stop")
                self.is_connected = False
                self.axis_x = 0.0
                self.axis_y = 0.0
                if self.on_disconnect:
                    self.on_disconnect()
                time.sleep(1.0)
            except Exception as e:
                logger.error(f"Error in gamepad reader loop: {e}")
                time.sleep(0.5)

    def get_axes(self) -> tuple[float, float]:
        """Returns normalized (X, Y) stick values."""
        return self.axis_x, self.axis_y

