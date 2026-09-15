import os
import json
from pathlib import Path
from typing import Any, Dict
from src.logger import logger

DEFAULT_CONFIG: Dict[str, Any] = {
    "network": {
        "esp32_ip": "192.168.50.2",
        "udp_port": 5005,
        "packet_rate": 50
    },
    "controller": {
        "deadzone": 0.10,
        "invert_throttle": True,
        "invert_steering": False,
        "max_speed": 100,
        "acceleration_step": 10
    },
    "safety": {
        "failsafe_ms": 300,
        "emergency_buttons": ["BTN_START", "BTN_SELECT"]
    }
}

class ConfigManager:
    def __init__(self, config_path: str = None):
        if config_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            self.config_path = base_dir / "config" / "controller.json"
        else:
            self.config_path = Path(config_path)

        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or uses defaults if missing/corrupt."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}. Using defaults.")
            self.data = DEFAULT_CONFIG.copy()
            self.save()
            return self.data

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                self.data = DEFAULT_CONFIG.copy()
                
                # Deep merge with defaults
                for section in ["network", "controller", "safety"]:
                    if section in loaded_data and isinstance(loaded_data[section], dict):
                        self.data[section].update(loaded_data[section])
                        
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to parse config file: {e}. Falling back to defaults.")
            self.data = DEFAULT_CONFIG.copy()

        return self.data

    def save(self) -> bool:
        """Saves current configuration to JSON file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"Saved configuration to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    @property
    def network(self) -> Dict[str, Any]:
        return self.data.get("network", DEFAULT_CONFIG["network"])

    @property
    def controller(self) -> Dict[str, Any]:
        return self.data.get("controller", DEFAULT_CONFIG["controller"])

    @property
    def safety(self) -> Dict[str, Any]:
        return self.data.get("safety", DEFAULT_CONFIG["safety"])
