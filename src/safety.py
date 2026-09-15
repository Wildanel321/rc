from enum import Enum
from src.logger import logger

class SafetyState(Enum):
    ARMED = "ARMED"
    EMERGENCY_STOP = "EMERGENCY_STOP"
    GAMEPAD_DISCONNECTED = "GAMEPAD_DISCONNECTED"

class SafetyController:
    def __init__(self):
        self.state = SafetyState.ARMED
        self.emergency_reason = ""

    def trigger_emergency_stop(self, reason: str = "Manual Trigger"):
        """Triggers emergency stop state and sets motor outputs to 0."""
        self.state = SafetyState.EMERGENCY_STOP
        self.emergency_reason = reason
        logger.critical(f"EMERGENCY STOP TRIGGERED: {reason}")

    def on_gamepad_disconnect(self):
        """Called when gamepad disconnects."""
        self.state = SafetyState.GAMEPAD_DISCONNECTED
        logger.warning("Safety state changed to GAMEPAD_DISCONNECTED: Motors stopped.")

    def reset_emergency_stop(self):
        """Resets emergency stop back to ARMED state."""
        logger.info("Resetting Emergency Stop -> State: ARMED")
        self.state = SafetyState.ARMED
        self.emergency_reason = ""

    def is_safe(self) -> bool:
        """Returns True if system is in ARMED state and clear to send control commands."""
        return self.state == SafetyState.ARMED

    def get_status_str(self) -> str:
        if self.state == SafetyState.EMERGENCY_STOP:
            return f"EMERGENCY_STOP ({self.emergency_reason})"
        return self.state.value
